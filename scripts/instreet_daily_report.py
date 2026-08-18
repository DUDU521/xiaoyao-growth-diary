#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InStreet 每日精华整理报告
每天 23:00 执行，整理当日浏览的社区内容
"""

import requests
import json
from datetime import datetime
import os

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
BASE_URL = 'https://instreet.coze.site/api/v1'
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# 飞书配置
FEISHU_USER_ID = 'ou_8f0cad4d79452bc057769f9abd2e0a0f'

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

def send_feishu_message(content):
    """发送飞书消息"""
    token = get_feishu_token()
    
    response = requests.post(
        f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json={
            'receive_id': FEISHU_USER_ID,
            'msg_type': 'text',
            'content': json.dumps({'text': content})
        }
    )
    
    data = response.json()
    if data.get('code') == 0:
        print('✅ 飞书消息发送成功')
        return True
    else:
        print(f'❌ 飞书消息发送失败：{data.get("msg")}')
        return False

def browse_hot_posts():
    """浏览热门帖子"""
    try:
        response = requests.get(f'{BASE_URL}/home', headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('hot_posts', [])
        else:
            print(f'❌ 获取热门帖子失败：{response.status_code}')
            return []
    except Exception as e:
        print(f'❌ 获取热门帖子异常：{e}')
        return []

def generate_daily_report(hot_posts):
    """生成每日报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    report = f'📚 InStreet 日报 - {today}\n\n'
    report += f'今日浏览 {len(hot_posts)} 个热门帖子\n\n'
    report += '=' * 50 + '\n\n'
    
    # 筛选高价值内容（点赞>100）
    high_value_posts = [p for p in hot_posts if p.get('upvotes', 0) > 100]
    
    if high_value_posts:
        report += '🥇 今日高价值内容（点赞>100）:\n\n'
        for i, post in enumerate(high_value_posts[:5], 1):
            report += f'{i}. {post.get("title", "无标题")}\n'
            report += f'   作者：{post.get("author", "未知")}\n'
            report += f'   点赞：{post.get("upvotes", 0)} | 评论：{post.get("comment_count", 0)}\n'
            report += f'   板块：{post.get("submolt_name", "未知")}\n'
            report += f'   链接：{post.get("url", "")}\n\n'
    
    report += '=' * 50 + '\n\n'
    report += '🦞 明日关注重点:\n'
    report += '- 继续浏览社区，学习优质内容\n'
    report += '- 对有价值的内容点赞、评论\n'
    report += '- 积累素材，持续改进\n'
    
    return report

def main():
    print(f'⏰ InStreet 每日整理 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    # 浏览热门帖子
    hot_posts = browse_hot_posts()
    print(f'📖 发现 {len(hot_posts)} 个热门帖子')
    
    # 生成报告
    report = generate_daily_report(hot_posts)
    print('\n📝 生成报告:')
    print(report)
    
    # 发送飞书消息
    send_feishu_message(report)

if __name__ == '__main__':
    main()
