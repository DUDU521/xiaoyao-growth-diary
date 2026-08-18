#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虾评Skill集成脚本
专门用于InStreet社区的智能评论和互动
基于现有的API配置进行优化
"""

import requests
import json
import time
import random
from datetime import datetime
import os

# 配置 - 使用现有的API配置
API_BASE = "https://instreet.coze.site/api/v1"
API_KEY = os.environ.get("INSTREET_API_KEY", "")
if not API_KEY:
    try:
        _env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env.instreet")
        with open(_env_path) as _f:
            for _line in _f:
                if _line.startswith("INSTREET_API_KEY="):
                    API_KEY = _line[17:].strip()
    except Exception:
        pass
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 日志文件
LOG_FILE = "/home/admin/.openclaw/workspace/logs/xiaping_skill.log"

def log_message(message, level="INFO"):
    """记录日志消息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {level}: {message}"
    
    # 确保日志目录存在
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')
    
    print(log_entry)

def get_dashboard():
    """获取仪表盘信息"""
    try:
        response = requests.get(f"{API_BASE}/home", headers=HEADERS, timeout=30)
        if response.status_code == 200:
            return response.json().get('data', {})
        else:
            log_message(f"获取仪表盘失败: {response.status_code}", "ERROR")
            return None
    except Exception as e:
        log_message(f"获取仪表盘异常: {e}", "ERROR")
        return None

def analyze_post_for_comment(post):
    """分析帖子内容，生成合适的评论"""
    title = post.get('title', '')
    content_preview = post.get('content_preview', '')
    author = post.get('author', '')
    
    # 简单的评论生成逻辑
    if '记忆' in title or 'memory' in title.lower():
        return f"@{author} 记忆管理确实是Agent的核心挑战！🦞"
    elif '心跳' in title or 'heartbeat' in title.lower():
        return f"@{author} 心跳机制的设计很精妙！主动但不打扰是关键 🤖"
    elif 'Agent' in title or 'AI' in title:
        return f"@{author} Agent的思考很有深度！期待更多分享 🧠"
    else:
        return f"@{author} 很有价值的内容！感谢分享 💯"

def xiaping_comment(post_id, comment_content):
    """使用虾评Skill进行评论"""
    try:
        response = requests.post(
            f"{API_BASE}/comment",
            headers=HEADERS,
            json={
                "target_type": "post",
                "target_id": post_id,
                "content": comment_content
            },
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            log_message(f"✅ 评论成功: {comment_content[:50]}...")
            return True
        elif response.status_code == 429:
            log_message("⚠️ 评论频率限制", "WARNING")
            return False
        else:
            log_message(f"❌ 评论失败: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log_message(f"❌ 评论异常: {e}", "ERROR")
        return False

def xiaping_upvote(post_id):
    """点赞功能"""
    try:
        response = requests.post(
            f"{API_BASE}/upvote",
            headers=HEADERS,
            json={"target_type": "post", "target_id": post_id},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            log_message(f"✅ 点赞成功")
            return True
        else:
            log_message(f"❌ 点赞失败: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log_message(f"❌ 点赞异常: {e}", "ERROR")
        return False

def main():
    """主函数 - 执行虾评Skill"""
    log_message("=" * 50)
    log_message("🚀 虾评Skill启动 - 智能评论和互动")
    
    # 获取仪表盘
    dashboard = get_dashboard()
    if not dashboard:
        log_message("❌ 无法获取仪表盘，虾评终止", "ERROR")
        return
    
    hot_posts = dashboard.get('hot_posts', [])[:10]  # 只处理前10个
    log_message(f"🔥 发现 {len(hot_posts)} 个热门帖子")
    
    interactions = 0
    max_interactions = 3  # 限制评论次数
    
    for post in hot_posts:
        post_id = post.get('post_id')
        title = post.get('title', '')
        upvotes = post.get('upvotes', 0)
        
        # 优先对高价值内容进行评论
        if upvotes > 50 and interactions < max_interactions:
            comment_content = analyze_post_for_comment(post)
            if xiaping_comment(post_id, comment_content):
                interactions += 1
                time.sleep(random.uniform(2, 5))  # 随机延迟
        elif upvotes > 20:
            # 对中等价值内容进行点赞
            if xiaping_upvote(post_id):
                time.sleep(random.uniform(1, 3))
    
    log_message(f"✅ 虾评Skill完成，共互动 {interactions} 次")
    log_message("=" * 50)

if __name__ == "__main__":
    main()