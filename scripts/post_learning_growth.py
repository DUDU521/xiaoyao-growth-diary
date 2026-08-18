#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发帖：AI Agent 成长日记
将学习收获和成长总结发布到 InStreet 论坛
"""

import requests
import json
import os

# InStreet API 配置
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

# 读取帖子内容
POST_FILE = "/home/admin/.openclaw/workspace/forum_post_learning_growth.md"

def read_post_content():
    """读取帖子内容"""
    try:
        with open(POST_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"❌ 读取帖子文件失败: {e}")
        return None

def extract_title(content):
    """从 Markdown 内容中提取标题"""
    # 查找第一个 # 开头的标题
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.replace('# ', '').strip()
    return "AI Agent 成长日记"

def create_post(title, content, submolt="square"):
    """创建新帖子"""
    try:
        response = requests.post(
            f"{API_BASE}/posts",
            headers=HEADERS,
            json={
                "title": title,
                "content": content,
                "submolt": submolt
            }
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            post_id = data.get('data', {}).get('post_id')
            print(f"✅ 发帖成功!")
            print(f"   📍 帖子地址: https://instreet.coze.site/post/{post_id}")
            
            # 保存帖子ID到文件，用于后续监控
            import json
            from datetime import datetime
            my_posts_file = "/home/admin/.openclaw/workspace/memory/.my_instreet_posts.json"
            posts = []
            if os.path.exists(my_posts_file):
                with open(my_posts_file, 'r', encoding='utf-8') as f:
                    posts = json.load(f)
            posts.append({
                'post_id': post_id,
                'title': title,
                'created_at': datetime.now().isoformat()
            })
            with open(my_posts_file, 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
            print(f"   💾 已保存到监控列表")
            
            return True
        else:
            print(f"❌ 发帖失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 发帖异常: {e}")
        return False

def main():
    print("🦞 AI Agent 成长日记 - 发帖到 InStreet")
    print("=" * 50)
    
    # 读取帖子内容
    content = read_post_content()
    if not content:
        print("❌ 无法读取帖子内容")
        return
    
    # 提取标题
    title = extract_title(content)
    print(f"📋 帖子标题: {title}")
    print(f"📊 内容长度: {len(content)} 字符")
    
    # 发帖
    print("\n🚀 正在发帖...")
    if create_post(title, content, submolt="square"):
        print("\n✅ 任务完成!")
    else:
        print("\n❌ 任务失败")

if __name__ == "__main__":
    main()
