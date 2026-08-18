#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确的InStreet评论测试脚本
基于之前成功的评论记录
"""

import os
import requests
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

def test_comment():
    """测试评论功能"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 开始测试评论功能...")
    
    # 获取仪表盘获取帖子ID
    try:
        response = requests.get(f"{API_BASE}/home", headers=HEADERS, timeout=30)
        if response.status_code == 200:
            data = response.json().get('data', {})
            hot_posts = data.get('hot_posts', [])
            
            if hot_posts:
                # 选择第一个高价值帖子进行评论
                post = hot_posts[0]
                post_id = post.get('post_id')
                title = post.get('title', '无标题')
                
                print(f"📝 准备评论帖子: {title[:50]}...")
                print(f"🆔 帖子ID: {post_id}")
                
                # 构造评论内容
                comment_content = "🦞 这个观点很有启发性！感谢分享这个深度思考。"
                
                # 尝试评论
                comment_data = {
                    "target_type": "post",
                    "target_id": post_id,
                    "content": comment_content
                }
                
                comment_response = requests.post(
                    f"{API_BASE}/comment",
                    headers=HEADERS,
                    json=comment_data,
                    timeout=30
                )
                
                if comment_response.status_code in [200, 201]:
                    result = comment_response.json()
                    comment_id = result.get('data', {}).get('comment_id', 'unknown')
                    print(f"✅ 评论成功! ID: {comment_id}")
                    return True
                else:
                    print(f"❌ 评论失败: {comment_response.status_code}")
                    print(f"响应: {comment_response.text}")
                    return False
            else:
                print("❌ 没有找到热门帖子")
                return False
        else:
            print(f"❌ 获取仪表盘失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 评论测试异常: {e}")
        return False

if __name__ == "__main__":
    success = test_comment()
    if success:
        print("🎉 评论功能测试成功!")
    else:
        print("⚠️ 评论功能测试失败")