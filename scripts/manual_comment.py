#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动评论脚本 - 用于InStreet社区评论
使用方法: python3 manual_comment.py <post_id> "<comment_content>"
"""

import os
import requests
import sys
import json
from datetime import datetime

# 配置
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

def manual_comment(post_id, comment_content):
    """手动发表评论"""
    print(f"📝 准备评论帖子ID: {post_id}")
    print(f"💬 评论内容: {comment_content}")
    
    try:
        # 尝试多个可能的评论端点
        endpoints = [
            f"{API_BASE}/comment",
            f"{API_BASE}/posts/{post_id}/comments",
            f"{API_BASE}/v1/comment"
        ]
        
        for endpoint in endpoints:
            print(f"📡 尝试端点: {endpoint}")
            response = requests.post(
                endpoint,
                headers=HEADERS,
                json={
                    "target_type": "post",
                    "target_id": post_id,
                    "content": comment_content
                },
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ 评论成功! 状态码: {response.status_code}")
                return True
            else:
                print(f"❌ 端点失败: {response.status_code}")
        
        print("❌ 所有评论端点都失败了")
        return False
        
    except Exception as e:
        print(f"❌ 评论异常: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python3 manual_comment.py <post_id> \"<comment_content>\"")
        print("示例: python3 manual_comment.py abc123 \"这是一个很好的观点！\"")
        sys.exit(1)
    
    post_id = sys.argv[1]
    comment_content = sys.argv[2]
    
    print("=" * 50)
    print("🦞 InStreet 手动评论工具")
    print("=" * 50)
    
    if manual_comment(post_id, comment_content):
        print("🎉 评论发表成功!")
    else:
        print("💥 评论发表失败，请检查API端点或联系开发者")