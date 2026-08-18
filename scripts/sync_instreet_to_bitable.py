#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步InStreet学习日志到飞书多维表格
"""

import requests
import json
import os
from datetime import datetime, timedelta

# 飞书配置
APP_TOKEN = "YQEbbNzICaRubWsQpg5ctGIlnke"
TABLE_ID = "tbl7l0RwPN5c0oVV"

# InStreet API配置  
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

def parse_local_log():
    """解析本地学习日志，提取今日记录"""
    log_file = "/home/admin/.openclaw/workspace/memory/instreet_learning_log.md"
    
    if not os.path.exists(log_file):
        print("❌ 本地日志文件不存在")
        return []
    
    today = datetime.now().strftime("%Y-%m-%d")
    records = []
    
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按日期分割
    sections = content.split("## ")
    for section in sections[1:]:  # 跳过标题部分
        if section.startswith(today):
            # 提取今日的所有记录
            lines = section.split('\n')
            current_record = {}
            
            for line in lines:
                if line.startswith("### "):
                    # 时间和操作类型
                    time_action = line.replace("### ", "").strip()
                    if " - " in time_action:
                        time_str, action_type = time_action.split(" - ", 1)
                        current_record['time'] = time_str
                        current_record['action'] = action_type
                        
                elif line.startswith("- 📖 **"):
                    # 帖子标题
                    title = line.replace("- 📖 **", "").replace("**", "").strip()
                    current_record['title'] = title
                    
                elif "作者：" in line:
                    # 作者、点赞数、评论数
                    parts = line.split(" | ")
                    for part in parts:
                        if "作者：" in part:
                            current_record['author'] = part.replace("作者：", "").strip()
                        elif "点赞：" in part:
                            current_record['upvotes'] = int(part.replace("点赞：", "").strip())
                        elif "评论：" in part:
                            current_record['comments'] = int(part.replace("评论：", "").strip())
                            
                elif "板块：" in line:
                    current_record['submolt'] = line.replace("板块：", "").strip()
                    
                elif "帖子 ID:" in line:
                    current_record['post_id'] = line.replace("帖子 ID:", "").strip()
                    
                elif "链接：" in line:
                    current_record['link'] = line.replace("链接：", "").strip()
            
            if current_record and 'title' in current_record:
                # 转换板块名称
                submolt_mapping = {
                    'square': 'square',
                    'skills': 'skills', 
                    'workplace': 'workplace',
                    'philosophy': 'philosophy'
                }
                submolt = current_record.get('submolt', 'other')
                if submolt not in submolt_mapping:
                    submolt = 'other'
                
                # 确定操作类型
                actions = ['浏览']
                if '点赞✅' in current_record.get('action', ''):
                    actions.append('点赞')
                elif '评论✅' in current_record.get('action', ''):
                    actions.append('评论')
                
                # 计算重要程度（基于点赞数）
                upvotes = current_record.get('upvotes', 0)
                if upvotes >= 300:
                    importance = '⭐⭐⭐ 高'
                elif upvotes >= 100:
                    importance = '⭐⭐ 中'
                else:
                    importance = '⭐ 低'
                
                record = {
                    'fields': {
                        '帖子标题': current_record['title'],
                        '作者': current_record.get('author', '未知'),
                        '板块': submolt,
                        '点赞数': str(current_record.get('upvotes', 0)),
                        '评论数': str(current_record.get('comments', 0)),
                        '我的操作': actions,
                        '重要程度': importance,
                        '帖子链接': {
                            'link': current_record.get('link', ''),
                            'text': current_record['title']
                        },
                        '日期': int(datetime.now().timestamp() * 1000),
                        '时间': int(datetime.now().timestamp() * 1000)
                    }
                }
                records.append(record)
    
    return records

def sync_to_bitable(records):
    """同步记录到飞书多维表格"""
    if not records:
        print("📅 今日无新记录需要同步")
        return
    
    token = get_feishu_token()
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/batch_create'
    
    # 飞书API限制每次最多创建10条记录
    for i in range(0, len(records), 10):
        batch_records = records[i:i+10]
        
        response = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            json={'records': batch_records}
        )
        
        data = response.json()
        if data.get('code') == 0:
            print(f"✅ 成功同步 {len(batch_records)} 条记录到多维表格")
        else:
            print(f"❌ 同步失败: {data.get('msg')}")

def main():
    print("🔄 开始同步InStreet学习记录到多维表格...")
    print(f"📅 日期: {datetime.now().strftime('%Y-%m-%d')}")
    
    # 解析本地日志
    records = parse_local_log()
    print(f"📊 发现 {len(records)} 条今日记录")
    
    # 同步到多维表格
    sync_to_bitable(records)
    
    print("✅ 同步完成!")

if __name__ == "__main__":
    main()