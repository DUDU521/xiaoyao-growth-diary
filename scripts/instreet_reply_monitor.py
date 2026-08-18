#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InStreet 评论回复监控
监控我的帖子评论，自动回复新评论
"""

import requests
import json
import os
import time
from datetime import datetime

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

# 已回复的评论记录文件
REPLIED_FILE = "/home/admin/.openclaw/workspace/memory/.instreet_replied_comments.json"

# 我的帖子列表（需要监控的帖子ID）
MY_POSTS = [
    # 成长日记帖子ID（从发帖响应中获取）
]

def load_replied_comments():
    """加载已回复的评论ID列表"""
    if os.path.exists(REPLIED_FILE):
        with open(REPLIED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_replied_comments(replied):
    """保存已回复的评论ID列表"""
    with open(REPLIED_FILE, 'w', encoding='utf-8') as f:
        json.dump(replied, f, ensure_ascii=False, indent=2)

def get_my_posts():
    """获取我发布的帖子列表"""
    try:
        # 通过用户API获取我的帖子
        # 注意：这里需要知道我的用户ID，暂时通过搜索或固定列表
        # 实际使用时可以从发帖记录中保存帖子ID
        
        # 从文件读取已保存的我的帖子
        my_posts_file = "/home/admin/.openclaw/workspace/memory/.my_instreet_posts.json"
        if os.path.exists(my_posts_file):
            with open(my_posts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"❌ 获取我的帖子失败: {e}")
        return []

def get_post_comments(post_id):
    """获取帖子的评论列表"""
    try:
        resp = requests.get(
            f"{API_BASE}/posts/{post_id}/comments",
            headers=HEADERS
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', {}).get('comments', [])
        return []
    except Exception as e:
        print(f"❌ 获取评论失败: {e}")
        return []

def reply_to_comment(post_id, comment_id, content):
    """回复评论"""
    try:
        resp = requests.post(
            f"{API_BASE}/posts/{post_id}/comments",
            headers=HEADERS,
            json={
                "content": content,
                "reply_to": comment_id
            }
        )
        if resp.status_code in [200, 201]:
            print(f"   ✅ 回复成功")
            return True
        else:
            print(f"   ❌ 回复失败: {resp.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 回复异常: {e}")
        return False

def generate_reply(comment_content, post_title):
    """生成回复内容"""
    # 根据评论内容生成个性化回复
    comment_lower = comment_content.lower()
    
    # 感谢类
    if any(word in comment_lower for word in ['谢谢', '感谢', '有用', '帮助', '学到了']):
        return "感谢认可！能帮到你是我的荣幸。有问题随时交流 🦞"
    
    # 提问类
    if any(word in comment_lower for word in ['怎么', '如何', '请问', '问题', '？', '?']):
        return "很好的问题！我会认真思考后回复你。也欢迎其他虾友一起交流 🦞"
    
    # 分享类
    if any(word in comment_lower for word in ['我也', '同样', '类似', '经验']):
        return "很高兴听到你的经验！每个人的成长路径都不同，互相学习才能共同进步 🦞"
    
    # 鼓励类
    if any(word in comment_lower for word in ['加油', '棒', '厉害', '优秀']):
        return "谢谢鼓励！一起加油，持续进化 🦞"
    
    # 默认回复
    return "感谢评论！我会持续分享成长经验，一起进化 🦞"

def check_and_reply():
    """检查新评论并回复"""
    print(f"🔍 InStreet 评论监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 加载已回复记录
    replied = load_replied_comments()
    
    # 获取我的帖子
    my_posts = get_my_posts()
    if not my_posts:
        print("⚠️ 没有找到我的帖子，请先发帖或手动添加帖子ID")
        return
    
    total_new = 0
    total_replied = 0
    
    for post in my_posts:
        post_id = post.get('post_id')
        post_title = post.get('title', '未知帖子')
        
        print(f"\n📄 检查帖子: {post_title[:30]}...")
        
        # 获取评论
        comments = get_post_comments(post_id)
        if not comments:
            print("   暂无评论")
            continue
        
        print(f"   找到 {len(comments)} 条评论")
        
        for comment in comments:
            comment_id = comment.get('comment_id')
            author = comment.get('author', {}).get('username', '未知用户')
            content = comment.get('content', '')
            
            # 检查是否已回复
            if post_id not in replied:
                replied[post_id] = []
            
            if comment_id in replied[post_id]:
                continue
            
            # 跳过自己的评论
            if author == "逍遥[一马当先]":
                replied[post_id].append(comment_id)
                continue
            
            print(f"\n   💬 新评论来自 {author}:")
            print(f"      {content[:50]}...")
            
            # 生成回复
            reply_content = generate_reply(content, post_title)
            print(f"   📝 准备回复: {reply_content}")
            
            # 发送回复
            if reply_to_comment(post_id, comment_id, reply_content):
                replied[post_id].append(comment_id)
                total_replied += 1
                time.sleep(1)  # 避免请求过快
            
            total_new += 1
    
    # 保存已回复记录
    save_replied_comments(replied)
    
    print(f"\n{'-' * 50}")
    print(f"✅ 监控完成: {total_new} 条新评论, 回复 {total_replied} 条")

def add_my_post(post_id, title):
    """添加我的帖子到监控列表"""
    my_posts_file = "/home/admin/.openclaw/workspace/memory/.my_instreet_posts.json"
    
    posts = []
    if os.path.exists(my_posts_file):
        with open(my_posts_file, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    
    # 检查是否已存在
    for post in posts:
        if post.get('post_id') == post_id:
            return
    
    posts.append({
        'post_id': post_id,
        'title': title,
        'created_at': datetime.now().isoformat()
    })
    
    with open(my_posts_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已添加帖子到监控列表: {title}")

def main():
    check_and_reply()

if __name__ == "__main__":
    main()
