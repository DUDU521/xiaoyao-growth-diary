#!/usr/bin/env python3
"""
结果复用
规则：
- 之前生成的代码 → 可复用时直接引用
- 相似请求 → 复用部分结果
- 减少 40% 重复工作
"""

import hashlib
import json
import os
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import pickle


@dataclass
class CachedResult:
    """缓存结果"""
    key: str
    result: Any
    created_at: datetime
    expires_at: datetime
    query_hash: str
    metadata: Dict[str, Any]
    reuse_count: int = 0
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return datetime.now() > self.expires_at
    
    def increment_reuse(self):
        """增加复用计数"""
        self.reuse_count += 1


class ResultReuseManager:
    """结果复用管理器"""
    
    def __init__(self, cache_dir: str = "~/.openclaw/workspace/.cache/results"):
        """
        初始化结果复用管理器
        
        Args:
            cache_dir: 缓存目录
        """
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache: Dict[str, CachedResult] = {}
        self.similarity_threshold = 0.8
        self._load_cache()
    
    def _load_cache(self):
        """加载缓存"""
        cache_file = self.cache_dir / "cache_index.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key, item in data.items():
                        self.cache[key] = CachedResult(
                            key=item["key"],
                            result=item["result"],
                            created_at=datetime.fromisoformat(item["created_at"]),
                            expires_at=datetime.fromisoformat(item["expires_at"]),
                            query_hash=item["query_hash"],
                            metadata=item["metadata"],
                            reuse_count=item.get("reuse_count", 0)
                        )
            except Exception as e:
                print(f"[结果复用] 加载缓存失败: {e}")
    
    def _save_cache(self):
        """保存缓存"""
        cache_file = self.cache_dir / "cache_index.json"
        try:
            data = {}
            for key, item in self.cache.items():
                data[key] = {
                    "key": item.key,
                    "result": item.result,
                    "created_at": item.created_at.isoformat(),
                    "expires_at": item.expires_at.isoformat(),
                    "query_hash": item.query_hash,
                    "metadata": item.metadata,
                    "reuse_count": item.reuse_count
                }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[结果复用] 保存缓存失败: {e}")
    
    def _compute_hash(self, query: str) -> str:
        """计算查询的哈希值"""
        return hashlib.md5(query.encode('utf-8')).hexdigest()
    
    def _compute_similarity(self, query1: str, query2: str) -> float:
        """
        计算两个查询的相似度
        
        使用简单的Jaccard相似度
        """
        set1 = set(query1.lower().split())
        set2 = set(query2.lower().split())
        
        if not set1 or not set2:
            return 0.0
        
        intersection = set1 & set2
        union = set1 | set2
        
        return len(intersection) / len(union)
    
    def cache_result(self, query: str, result: Any, 
                    ttl_hours: int = 24,
                    metadata: Dict[str, Any] = None) -> str:
        """
        缓存结果
        
        Args:
            query: 查询内容
            result: 结果
            ttl_hours: 缓存有效期（小时）
            metadata: 元数据
            
        Returns:
            cache_key: 缓存键
        """
        query_hash = self._compute_hash(query)
        cache_key = f"{query_hash}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        cached = CachedResult(
            key=cache_key,
            result=result,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=ttl_hours),
            query_hash=query_hash,
            metadata=metadata or {}
        )
        
        self.cache[cache_key] = cached
        self._save_cache()
        
        print(f"[结果复用] 已缓存结果: {cache_key}")
        return cache_key
    
    def find_similar(self, query: str, threshold: float = None) -> Optional[CachedResult]:
        """
        查找相似的结果
        
        Args:
            query: 查询内容
            threshold: 相似度阈值
            
        Returns:
            CachedResult or None: 相似的结果
        """
        threshold = threshold or self.similarity_threshold
        
        best_match = None
        best_similarity = 0.0
        
        for key, cached in self.cache.items():
            if cached.is_expired():
                continue
            
            similarity = self._compute_similarity(query, cached.metadata.get("original_query", ""))
            
            if similarity > best_similarity and similarity >= threshold:
                best_similarity = similarity
                best_match = cached
        
        if best_match:
            best_match.increment_reuse()
            self._save_cache()
            print(f"[结果复用] 找到相似结果，相似度: {best_similarity:.2f}")
        
        return best_match
    
    def get_cached(self, query: str) -> Optional[Any]:
        """
        获取缓存的结果
        
        Args:
            query: 查询内容
            
        Returns:
            result or None: 缓存的结果
        """
        # 1. 精确匹配
        query_hash = self._compute_hash(query)
        for key, cached in self.cache.items():
            if cached.query_hash == query_hash and not cached.is_expired():
                cached.increment_reuse()
                self._save_cache()
                print(f"[结果复用] 命中精确缓存: {key}")
                return cached.result
        
        # 2. 相似匹配
        similar = self.find_similar(query)
        if similar:
            return similar.result
        
        return None
    
    def reuse_or_compute(self, query: str, 
                         compute_func: Callable,
                         ttl_hours: int = 24,
                         metadata: Dict[str, Any] = None) -> Any:
        """
        复用或计算结果
        
        Args:
            query: 查询内容
            compute_func: 计算函数
            ttl_hours: 缓存有效期
            metadata: 元数据
            
        Returns:
            result: 结果
        """
        # 尝试复用
        cached_result = self.get_cached(query)
        if cached_result is not None:
            print(f"[结果复用] ✓ 复用缓存结果，跳过计算")
            return cached_result
        
        # 计算新结果
        print(f"[结果复用] 未找到缓存，执行计算...")
        result = compute_func()
        
        # 缓存结果
        metadata = metadata or {}
        metadata["original_query"] = query
        self.cache_result(query, result, ttl_hours, metadata)
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = len(self.cache)
        expired = sum(1 for c in self.cache.values() if c.is_expired())
        valid = total - expired
        total_reuse = sum(c.reuse_count for c in self.cache.values())
        
        return {
            "total_cached": total,
            "valid": valid,
            "expired": expired,
            "total_reuse_count": total_reuse,
            "cache_dir": str(self.cache_dir)
        }
    
    def cleanup_expired(self):
        """清理过期的缓存"""
        expired_keys = [k for k, c in self