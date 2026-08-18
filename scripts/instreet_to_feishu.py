#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InStreet 学习内容自动填入飞书多维表格
每次心跳后自动执行，实时记录
"""

import os
import requests
import json
from datetime import datetime
import time

# 飞书多维表格配置
APP_TOKEN = "YQEbbNzICaRubWsQpg5ctGIlnke"
TABLE_ID = "tbl7l0RwPN5c0oVV"

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

def get_feishu_token():
    """获取飞书 tenant_access_token"""
    config_path = '/home/admin/.openclaw/openclaw.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    app_id = config['channels']['feishu']['accounts']['default']['appId']
    app_secret = config['channels']['feishu']['accounts']['default']['appSecret']
    
    response = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': app_id, 'app_secret': app_secret}
    )
    data = response.json()
    return data.get('tenant_access_token')

def create_record(fields):
    """创建记录到多维表格"""
    token = get_feishu_token()
    
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'fields': fields
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if result.get('code') == 0:
        print(f'✅ 记录已填入表格：{fields.get("帖子标题", "")[:30]}...')
        return True
    else:
        print(f'❌ 填入表格失败：{result.get("msg", "")}')
        print(f'   响应：{response.text[:200]}')
        return False

def browse_and_record(max_records=5):
    """浏览热门帖子并记录到表格"""
    print(f'🌐 开始浏览 InStreet 并记录到表格...')
    
    # 获取热门帖子
    response = requests.get(f'{API_BASE}/home', headers=HEADERS)
    if response.status_code != 200:
        print(f'❌ 获取热门帖子失败：{response.status_code}')
        return 0
    
    data = response.json()
    hot_posts = data.get('data', {}).get('hot_posts', [])
    print(f'🔥 发现 {len(hot_posts)} 个热门帖子')
    
    recorded_count = 0
    
    for post in hot_posts[:15]:  # 浏览前 15 个
        post_id = post.get('post_id')
        title = post.get('title', '无标题')
        author = post.get('author', '未知')
        upvotes = post.get('upvotes', 0)
        comment_count = post.get('comment_count', 0)
        submolt = post.get('submolt_name', 'other')
        url = f'https://instreet.coze.site/post/{post_id}'
        
        # 确定重要程度
        if upvotes > 200:
            importance = '⭐⭐⭐ 高'
        elif upvotes > 100:
            importance = '⭐⭐ 中'
        else:
            importance = '⭐ 低'
        
        # 准备字段
        now = datetime.now()
        fields = {
            '日期': int(now.timestamp() * 1000),
            '时间': int(now.timestamp() * 1000),
            '帖子标题': title,
            '作者': author,
            '板块': submolt if submolt in ['skills', 'square', 'workplace', 'philosophy'] else 'other',
            '点赞数': upvotes,
            '评论数': comment_count,
            '我的操作': ['浏览'],
            '重要程度': importance,
            '帖子链接': {'link': url, 'text': title}
        }
        
        # 对高价值内容点赞
        if upvotes > 50 and recorded_count < max_records:
            try:
                like_response = requests.post(
                    f'{API_BASE}/upvote',
                    headers=HEADERS,
                    json={'target_type': 'post', 'target_id': post_id}
                )
                if like_response.status_code in [200, 201]:
                    fields['我的操作'] = ['浏览', '点赞']
                    print(f'   ✅ 点赞：{title[:30]}... ({upvotes}赞)')
                    time.sleep(1)  # 避免频率限制
            except Exception as e:
                print(f'   ⚠️ 点赞失败：{e}')
        
        # 创建记录
        if create_record(fields):
            recorded_count += 1
    
    return recorded_count

def main():
    print(f'⏰ InStreet 表格记录 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 50)
    
    count = browse_and_record()
    
    print('=' * 50)
    print(f'✅ 完成，共记录 {count} 条内容到表格')
    print(f'📊 表格地址：https://my.feishu.cn/base/{APP_TOKEN}')

if __name__ == '__main__':
    main()
