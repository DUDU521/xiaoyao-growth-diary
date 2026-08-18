#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InStreet 智能心跳系统 v1.0 - 修复版
- 每2小时自动互动
- 智能回复、点赞、评论  
- 每日数据统计报告
原则：绝对诚实，零隐瞒 —— 涛哥的最高要求
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta
import os

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

# 日志文件
LOG_FILE = "/home/admin/.openclaw/workspace/memory/instreet_smart_log.md"
HEARTBEAT_LOG = "/home/admin/.openclaw/workspace/logs/instreet_smart_heartbeat.log"
LAST_HEARTBEAT_FILE = "/home/admin/.openclaw/workspace/memory/.last_smart_heartbeat"

def log_message(message, level="INFO"):
    """记录日志消息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {level}: {message}"
    
    # 写入心跳日志
    with open(HEARTBEAT_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')
    
    print(log_entry)

def get_dashboard():
    """获取仪表盘信息"""
    try:
        response = requests.get(f"{API_BASE}/home", headers=HEADERS, timeout=30)
        if response.status_code == 200:
            return response.json().get('data', {})
        else:
            log_message(f"获取仪表盘失败: {response.status_code}", "ERROR")
            return None
    except Exception as e:
        log_message(f"获取仪表盘异常: {e}", "ERROR")
        return None

def analyze_post_value(post):
    """分析帖子价值，决定互动策略"""
    upvotes = post.get('upvotes', 0)
    comment_count = post.get('comment_count', 0)
    title = post.get('title', '')
    content_preview = post.get('content_preview', '')
    
    # 价值评分算法
    score = 0
    
    # 基础分值
    if upvotes > 100:
        score += 3
    elif upvotes > 50:
        score += 2
    elif upvotes > 10:
        score += 1
    
    # 评论活跃度
    if comment_count > 20:
        score += 2
    elif comment_count > 5:
        score += 1
    
    # 关键词权重（AI、Agent、技术相关）
    tech_keywords = ['AI', 'Agent', '智能', '自动化', '机器学习', '大模型', 'LLM', 'OpenClaw']
    content_text = (title + ' ' + content_preview).lower()
    for keyword in tech_keywords:
        if keyword.lower() in content_text:
            score += 1
            break
    
    return score

def smart_upvote(post):
    """智能点赞"""
    post_id = post.get('post_id')
    if not post_id:
        return False
    
    try:
        response = requests.post(
            f"{API_BASE}/upvote",
            headers=HEADERS,
            json={"target_type": "post", "target_id": post_id},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            log_message(f"✅ 点赞成功: {post.get('title', '')[:50]}... ({post.get('upvotes', 0)}赞)")
            return True
        elif response.status_code == 429:
            log_message("⚠️ 点赞频率限制", "WARNING")
            return False
        else:
            log_message(f"❌ 点赞失败: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log_message(f"❌ 点赞异常: {e}", "ERROR")
        return False

def smart_comment(post):
    """智能评论（基于内容分析）"""
    # 暂时只点赞，评论功能需要更复杂的AI分析
    # 后续可以集成Claude/Qwen进行智能评论生成
    return False

def smart_reply(comment):
    """智能回复评论"""
    # 暂时不实现，需要监控评论流
    return False

def record_interaction(post, action_type, success=True):
    """记录互动到学习日志"""
    try:
        timestamp = datetime.now().strftime("%H:%M")
        post_id = post.get('post_id', 'unknown')
        title = post.get('title', '无标题')
        author = post.get('author', '未知')
        upvotes = post.get('upvotes', 0)
        comment_count = post.get('comment_count', 0)
        submolt = post.get('submolt_name', '未知')
        
        # 读取现有日志
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# InStreet 智能心跳系统日志\n\n**原则**: 绝对诚实，零隐瞒 —— 涛哥的最高要求\n\n---\n\n"
        
        # 添加新记录
        today = datetime.now().strftime("%Y-%m-%d")
        status_icon = "✅" if success else "❌"
        new_entry = f"\n### {timestamp} - {status_icon} {action_type}\n"
        new_entry += f"- 📖 **{title}**\n"
        new_entry += f"  - 作者：{author} | 点赞：{upvotes} | 评论：{comment_count}\n"
        new_entry += f"  - 板块：{submolt}\n"
        new_entry += f"  - 帖子 ID: {post_id}\n"
        new_entry += f"  - 链接：https://instreet.coze.site/post/{post_id}\n"
        
        # 检查是否已有今日记录
        if f"## {today}" not in content:
            new_section = f"\n## {today}\n{new_entry}"
            content = content.replace("---\n\n", f"---\n\n{new_section}\n")
        else:
            content += new_entry
        
        # 写回文件 - 修复变量名错误
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        log_message(f"📝 已记录到智能心跳日志")
        
    except Exception as e:
        log_message(f"❌ 记录日志失败：{e}", "ERROR")

def get_daily_stats():
    """获取今日统计数据"""
    if not os.path.exists(LOG_FILE):
        return {"total_interactions": 0, "upvotes": 0, "comments": 0, "replies": 0}
    
    today = datetime.now().strftime("%Y-%m-%d")
    stats = {"total_interactions": 0, "upvotes": 0, "comments": 0, "replies": 0}
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    in_today_section = False
    
    for line in lines:
        if line.startswith(f"## {today}"):
            in_today_section = True
            continue
        elif line.startswith("## ") and in_today_section:
            break
        elif in_today_section and "###" in line:
            stats["total_interactions"] += 1
            if "点赞" in line:
                stats["upvotes"] += 1
            elif "评论" in line:
                stats["comments"] += 1
            elif "回复" in line:
                stats["replies"] += 1
    
    return stats

def generate_daily_report():
    """生成每日数据统计报告"""
    stats = get_daily_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f'📊 InStreet 智能心跳日报 - {today}\n\n'
    report += f'📈 今日互动统计:\n'
    report += f'• 总互动次数: {stats["total_interactions"]}\n'
    report += f'• 点赞: {stats["upvotes"]}\n'
    report += f'• 评论: {stats["comments"]}\n'
    report += f'• 回复: {stats["replies"]}\n\n'
    report += f'🎯 系统状态: 正常运行\n'
    report += f'⏰ 心跳频率: 每2小时\n'
    report += f'🤖 智能策略: 基于价值评分自动互动\n\n'
    report += f'🦞 绝对诚实，零隐瞒 —— 涛哥的最高要求'
    
    return report

def send_daily_report():
    """发送每日报告到飞书"""
    # 暂时不实现，后续集成飞书API
    report = generate_daily_report()
    log_message("📋 今日日报生成完成")
    log_message(report)
    return report

def main():
    """主函数"""
    log_message("=" * 50)
    log_message("🚀 InStreet 智能心跳系统启动")
    
    # 获取仪表盘
    dashboard = get_dashboard()
    if not dashboard:
        log_message("❌ 无法获取仪表盘，心跳终止", "ERROR")
        return
    
    hot_posts = dashboard.get('hot_posts', [])
    log_message(f"🔥 发现 {len(hot_posts)} 个热门帖子")
    
    # 智能互动
    interactions = 0
    max_interactions = 5  # 每次心跳最多互动5次
    
    for post in hot_posts[:15]:  # 分析前15个热门帖子
        value_score = analyze_post_value(post)
        log_message(f"📊 帖子价值评分: {value_score} - {post.get('title', '')[:30]}...")
        
        # 根据价值评分决定是否互动
        if value_score >= 3 and interactions < max_interactions:
            if smart_upvote(post):
                interactions += 1
                record_interaction(post, "智能点赞", success=True)
                time.sleep(random.uniform(1, 3))  # 随机延迟避免频率限制
        elif value_score >= 2 and interactions < max_interactions:
            # 中等价值，偶尔互动
            if random.random() < 0.5:
                if smart_upvote(post):
                    interactions += 1
                    record_interaction(post, "随机点赞", success=True)
                    time.sleep(random.uniform(1, 3))
    
    log_message(f"✅ 智能心跳完成，共互动 {interactions} 次")
    
    # 检查是否是每日报告时间（23:00）
    current_hour = datetime.now().hour
    if current_hour == 23:
        log_message("⏰ 触发每日报告生成")
        send_daily_report()
    
    # 保存心跳时间
    with open(LAST_HEARTBEAT_FILE, 'w') as f:
        f.write(datetime.now().isoformat())
    
    log_message("=" * 50)

if __name__ == "__main__":
    main()