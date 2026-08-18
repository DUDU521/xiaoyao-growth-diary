#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InStreet 每日日报生成脚本
从飞书多维表格提取当日数据，生成日报发送
"""

import requests
import json
from datetime import datetime, timedelta

# 飞书多维表格配置
APP_TOKEN = "YQEbbNzICaRubWsQpg5ctGIlnke"
TABLE_ID = "tbl7l0RwPN5c0oVV"

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

def get_today_records():
    """获取今日记录"""
    token = get_feishu_token()
    
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 获取所有记录
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if data.get('code') != 0:
        print(f'❌ 获取记录失败：{data.get("msg")}')
        return []
    
    records = data.get('data', {}).get('items', [])
    
    # 筛选今日记录
    today = datetime.now().strftime('%Y-%m-%d')
    today_records = []
    
    for record in records:
        fields = record.get('fields', {})
        date_ts = fields.get('日期', 0)
        if date_ts:
            record_date = datetime.fromtimestamp(date_ts / 1000).strftime('%Y-%m-%d')
            if record_date == today:
                today_records.append(fields)
    
    return today_records

def generate_daily_report(records):
    """生成日报内容"""
    if not records:
        return '📚 InStreet 日报 - 今日无记录\n\n今天还没有浏览内容哦～'
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 统计
    total_browsed = len([r for r in records if '浏览' in r.get('我的操作', [])])
    total_liked = len([r for r in records if '点赞' in r.get('我的操作', [])])
    high_value = [r for r in records if r.get('重要程度') == '⭐⭐⭐ 高']
    medium_value = [r for r in records if r.get('重要程度') == '⭐⭐ 中']
    
    report = f'📚 InStreet 日报 - {today}\n\n'
    report += f'📊 今日统计:\n'
    report += f'• 浏览：{total_browsed} 篇\n'
    report += f'• 点赞：{total_liked} 篇\n'
    report += f'• 高价值：{len(high_value)} 篇\n'
    report += f'• 中价值：{len(medium_value)} 篇\n\n'
    report += '=' * 50 + '\n\n'
    
    # 高价值内容
    if high_value:
        report += '🥇 高价值内容推荐:\n\n'
        for i, rec in enumerate(high_value[:3], 1):
            title = rec.get('帖子标题', '无标题')
            author = rec.get('作者', '未知')
            upvotes = rec.get('点赞数', 0)
            link_obj = rec.get('帖子链接', {})
            link = link_obj.get('link', '') if isinstance(link_obj, dict) else link_obj
            
            report += f'{i}. {title}\n'
            report += f'   作者：{author} | 点赞：{upvotes}\n'
            report += f'   链接：{link}\n\n'
    
    # 所有记录列表
    report += '📖 完整浏览清单:\n\n'
    for i, rec in enumerate(records[:10], 1):  # 最多显示 10 条
        title = rec.get('帖子标题', '无标题')[:50]
        upvotes = rec.get('点赞数', 0)
        operations = '、'.join(rec.get('我的操作', ['浏览']))
        
        report += f'{i}. {title}...\n'
        report += f'   操作：{operations} | 点赞：{upvotes}\n\n'
    
    report += '=' * 50 + '\n\n'
    report += '🦞 明日计划:\n'
    report += '• 继续浏览 InStreet，学习优质内容\n'
    report += '• 对有价值的内容点赞、评论\n'
    report += '• 深度参与社区讨论\n\n'
    report += '📊 完整表格：https://my.feishu.cn/base/YQEbbNzICaRubWsQpg5ctGIlnke'
    
    return report

def send_feishu_message(content):
    """发送飞书消息"""
    token = get_feishu_token()
    
    user_id = 'ou_8f0cad4d79452bc057769f9abd2e0a0f'
    
    response = requests.post(
        f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json={
            'receive_id': user_id,
            'msg_type': 'text',
            'content': json.dumps({'text': content})
        }
    )
    
    data = response.json()
    if data.get('code') == 0:
        print('✅ 飞书日报发送成功')
        return True
    else:
        print(f'❌ 飞书日报发送失败：{data.get("msg")}')
        return False

def main():
    print(f'⏰ InStreet 日报生成 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 50)
    
    # 获取今日记录
    records = get_today_records()
    print(f'📊 发现 {len(records)} 条今日记录')
    
    # 生成报告
    report = generate_daily_report(records)
    print('\n📝 生成日报:')
    print(report)
    print('\n' + '=' * 50)
    
    # 发送消息
    send_feishu_message(report)

if __name__ == '__main__':
    main()
