#!/usr/bin/env python3
"""
时间片管理 - 长任务分段执行
规则：长时间任务 → 分成小块 → 每块 ≤ 30秒
"""

import time
from typing import Callable, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TaskChunk:
    """任务块"""
    id: int
    name: str
    func: Callable
    args: tuple
    kwargs: dict
    estimated_time: float  # 预估执行时间（秒）
    
class TaskScheduler:
    """任务调度器 - 实现时间片管理"""
    
    def __init__(self, max_chunk_time: float = 30.0):
        """
        初始化调度器
        
        Args:
            max_chunk_time: 每个任务块的最大执行时间（秒），默认30秒
        """
        self.max_chunk_time = max_chunk_time
        self.chunks: List[TaskChunk] = []
        self.results = {}
        self.completed = set()
        
    def add_chunk(self, name: str, func: Callable, *args, 
                  estimated_time: float = 10.0, **kwargs) -> int:
        """
        添加任务块
        
        Args:
            name: 任务块名称
            func: 执行函数
            args: 位置参数
            estimated_time: 预估执行时间
            kwargs: 关键字参数
            
        Returns:
            chunk_id: 任务块ID
        """
        chunk_id = len(self.chunks)
        chunk = TaskChunk(
            id=chunk_id,
            name=name,
            func=func,
            args=args,
            kwargs=kwargs,
            estimated_time=estimated_time
        )
        self.chunks.append(chunk)
        return chunk_id
    
    def execute_chunk(self, chunk_id: int) -> Any:
        """
        执行单个任务块
        
        Args:
            chunk_id: 任务块ID
            
        Returns:
            result: 执行结果
        """
        if chunk_id in self.completed:
            return self.results[chunk_id]
            
        chunk = self.chunks[chunk_id]
        start_time = time.time()
        
        print(f"[时间片管理] 开始执行任务块 {chunk_id}: {chunk.name}")
        print(f"[时间片管理] 预估时间: {chunk.estimated_time}秒")
        
        try:
            result = chunk.func(*chunk.args, **chunk.kwargs)
            elapsed = time.time() - start_time
            
            self.results[chunk_id] = result
            self.completed.add(chunk_id)
            
            print(f"[时间片管理] 任务块 {chunk_id} 完成，实际耗时: {elapsed:.2f}秒")
            
            # 检查是否超时
            if elapsed > self.max_chunk_time:
                print(f"[时间片管理] ⚠️ 警告: 任务块 {chunk_id} 超时！")
                
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[时间片管理] ❌ 任务块 {chunk_id} 失败: {str(e)}")
            raise
    
    def execute_all(self, report_progress: bool = True) -> dict:
        """
        执行所有任务块
        
        Args:
            report_progress: 是否报告进度
            
        Returns:
            results: 所有任务结果
        """
        total = len(self.chunks)
        print(f"[时间片管理] 开始执行 {total} 个任务块")
        print(f"[时间片管理] 每个任务块最大执行时间: {self.max_chunk_time}秒")
        print()
        
        for i, chunk in enumerate(self.chunks):
            if report_progress:
                progress = (i / total) * 100
                print(f"\n[时间片管理] 进度: {progress:.1f}% ({i}/{total})")
                
            self.execute_chunk(chunk.id)
            
        print(f"\n[时间片管理] 所有任务块执行完成！")
        return self.results
    
    def get_progress(self) -> dict:
        """获取当前进度"""
        total = len(self.chunks)
        completed = len(self.completed)
        return {
            "total": total,
            "completed": completed,
            "remaining": total - completed,
            "percentage": (completed / total * 100) if total > 0 else 0
        }
    
    def split_long_task(self, task_func: Callable, items: List[Any], 
                       chunk_size: int = 10) -> List[int]:
        """
        将长任务拆分为多个小块
        
        Args:
            task_func: 任务函数
            items: 要处理的项目列表
            chunk_size: 每个块处理的项目数
            
        Returns:
            chunk_ids: 生成的任务块ID列表
        """
        chunk_ids = []
        for i in range(0, len(items), chunk_size):
            chunk_items = items[i:i+chunk_size]
            chunk_id = self.add_chunk(
                name=f"处理项目 {i+1}-{min(i+chunk_size, len(items))}",
                func=task_func,
                args=(chunk_items,),
                estimated_time=5.0  # 预估每个小块5秒
            )
            chunk_ids.append(chunk_id)
        
        return chunk_ids


# 使用示例
def example_task(items):
    """示例任务：处理一批项目"""
    results = []
    for item in items:
        time.sleep(0.1)  # 模拟处理时间
        results.append(f"处理完成: {item}")
    return results


if __name__ == "__main__":
    # 示例：将100个项目的处理任务拆分为小块
    scheduler = TaskScheduler(max_chunk_time=30.0)
    
    items = list(range(1, 101))  # 100个项目
    
    # 拆分为每块10个项目
    chunk_ids = scheduler.split_long_task(example_task, items, chunk_size=10)
    
    print(f"已将任务拆分为 {len(chunk_ids)} 个任务块")
    print()
    
    # 执行所有任务块
    results = scheduler.execute_all()
    
    print(f"\n总计处理 {len(items)} 个项目")
