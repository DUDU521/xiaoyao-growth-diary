#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InStreet 智能心跳系统 - 每日统计报告 v3
自动生成详细的每日互动统计报告
"""

import requests
import json
from datetime import datetime, timedelta
import os

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

def generate_smart_report(records):
    """生成智能日报内容"""
    if not records:
        return '📚 InStreet 智能心跳日报 - 今日无记录\n\n今天还没有进行任何互动哦～'
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 统计各类互动
    total_interactions = len(records)
    likes = len([r for r in records if '点赞' in r.get('我的操作', [])])
    comments = len([r for r in records if '评论' in r.get('我的操作', [])])
    replies = len([r for r in records if '回复' in r.get('我的操作', [])])
    views = len([r for r in records if '浏览' in r.get('我的操作', [])])
    
    # 价值分析
    high_value = [r for r in records if r.get('重要程度') == '⭐⭐⭐ 高']
    medium_value = [r for r in records if r.get('重要程度') == '⭐⭐ 中']
    low_value = [r for r in records if r.get('重要程度') == '⭐ 低']
    
    # 主题分布
    topics = {}
    for r in records:
        topic = r.get('主题分类', '未知')
        topics[topic] = topics.get(topic, 0) + 1
    
    report = f'🤖 InStreet 智能心跳日报 - {today}\n\n'
    report += f'📊 今日互动统计:\n'
    report += f'• 总互动次数：{total_interactions} 次\n'
    report += f'• 浏览：{views} 次\n'
    report += f'• 点赞：{likes} 次\n'
    report += f'• 评论：{comments} 次\n'
    report += f'• 回复：{replies} 次\n\n'
    
    report += f'🎯 价值分布:\n'
    report += f'• 高价值内容：{len(high_value)} 篇\n'
    report += f'• 中价值内容：{len(medium_value)} 篇\n'
    report += f'• 低价值内容：{len(low_value)} 篇\n\n'
    
    report += f'📈 主题分布:\n'
    for topic, count in sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f'• {topic}：{count} 篇\n'
    
    report += '\n' + '=' * 50 + '\n\n'
    
    # 高价值内容推荐
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
    
    # 智能分析
    report += '🧠 智能分析:\n'
    if likes > 0 and comments == 0:
        report += '• 建议增加评论互动，提升社区参与度\n'
    if total_interactions < 10:
        report += '• 今日互动较少，建议增加浏览频率\n'
    if len(high_value) > 0:
        report += '• 高价值内容识别准确，继续保持！\n'
    
    report += '\n' + '=' * 50 + '\n\n'
    report += '🦞 明日计划:\n'
    report += '• 继续每2小时智能心跳\n'
    report += '• 优化评论质量，增加深度互动\n'
    report += '• 重点关注高价值内容创作者\n\n'
    report += '📊 完整数据：https://my.feishu.cn/base/YQEbbNzICaRubWsQpg5ctGIlnke'
    
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
    print(f'⏰ InStreet 智能日报生成 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 50)
    
    # 获取今日记录
    records = get_today_records()
    print(f'📊 发现 {len(records)} 条今日记录')
    
    # 生成报告
    report = generate_smart_report(records)
    print('\n📝 生成日报:')
    print(report)
    print('\n' + '=' * 50)
    
    # 发送消息
    send_feishu_message(report)

if __name__ == '__main__':
    main()