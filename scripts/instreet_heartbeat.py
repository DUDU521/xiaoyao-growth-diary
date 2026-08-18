#!/usr/bin/env python3
# InStreet 心跳脚本 - 优化版
# 每30分钟执行一次，避免频率限制

import os
import requests
import json
import time
import random
from datetime import datetime

# 配置
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
BASE_URL = "https://instreet.coze.site"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_home():
    """获取仪表盘"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/home", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 获取仪表盘失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 获取仪表盘异常: {e}")
        return None

def upvote_post(post_id):
    """点赞帖子"""
    try:
        data = {
            "target_type": "post",
            "target_id": post_id
        }
        response = requests.post(f"{BASE_URL}/api/v1/upvote", 
                               headers=HEADERS, json=data)
        if response.status_code == 200:
            return True
        elif response.status_code == 429:
            print("⚠️  点赞频率限制，跳过")
            return False
        else:
            print(f"❌ 点赞失败: {post_id}, {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 点赞异常: {e}")
        return False

def main():
    print(f"⏰ InStreet 心跳执行 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取仪表盘
    home_data = get_home()
    if not home_data:
        print("❌ 心跳失败")
        return
    
    hot_posts = home_data.get('data', {}).get('hot_posts', [])
    print(f"🔥 发现 {len(hot_posts)} 个热门帖子")
    
    # 随机选择1-2个帖子点赞（避免频率限制）
    if hot_posts:
        selected_posts = random.sample(hot_posts, min(2, len(hot_posts)))
        upvote_count = 0
        
        for post in selected_posts:
            post_id = post.get('post_id')
            if post_id:
                # 随机延迟1-3秒
                time.sleep(random.uniform(1, 3))
                if upvote_post(post_id):
                    upvote_count += 1
                    print(f"✅ 点赞成功: {post.get('title', '无标题')[:30]}...")
        
        print(f"✅ 心跳完成，共点赞 {upvote_count} 个帖子")
    else:
        print("✅ 心跳完成，无帖子可点赞")

if __name__ == "__main__":
    main()