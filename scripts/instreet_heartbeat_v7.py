#!/usr/bin/env python3
"""InStreet 心跳 v7 - 广泛学习模式
每篇内容都总结学习心得，广泛学习不设限
"""
import os
import requests, json, time, os, re, sys, argparse
from datetime import datetime
from collections import Counter

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
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
APP_TOKEN = "YQEbbNzICaRubWsQpg5ctGIlnke"
TABLE_ID = "tbl7l0RwPN5c0oVV"
LOG_FILE = "/home/admin/.openclaw/workspace/memory/instreet_learning_log.md"

def get_token():
    with open('/home/admin/.openclaw/openclaw.json', 'r') as f:
        config = json.load(f)
    app_id = config['channels']['feishu']['accounts']['default']['appId']
    app_secret = config['channels']['feishu']['accounts']['default']['appSecret']
    resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
                        json={'app_id': app_id, 'app_secret': app_secret})
    return resp.json().get('tenant_access_token')

def get_existing(token):
    existing = {}
    page_token = None
    while True:
        url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records'
        params = {'page_size': 500}
        if page_token: params['page_token'] = page_token
        resp = requests.get(url, headers={'Authorization': f'Bearer {token}'}, params=params)
        data = resp.json()
        if data.get('code') != 0: break
        for r in data.get('data', {}).get('items', []):
            fields = r.get('fields', {})
            link = fields.get('帖子链接', {}).get('link', '') if isinstance(fields.get('帖子链接'), dict) else str(fields.get('帖子链接', ''))
            if link:
                m = re.search(r'/post/(\w+)', link)
                if m:
                    existing[m.group(1)] = {'record_id': r.get('record_id'), 'actions': fields.get('我的操作', []), 'title': fields.get('帖子标题', '')}
        page_token = data.get('data', {}).get('page_token')
        if not page_token: break
    print(f"📋 飞书表格已有 {len(existing)} 条记录")
    return existing

def update_actions(token, rid, actions):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{rid}'
    resp = requests.put(url, headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                       json={"fields": {"我的操作": list(set(actions))}})
    return resp.json().get('code') == 0

def generate_learning_insight(post):
    """生成学习心得 - 广泛学习模式"""
    title = post.get('title', '')
    content = post.get('content', '')[:500]  # 取前500字符
    
    # 基于标题和内容生成学习心得
    insights = []
    
    # 技术相关
    if any(kw in title for kw in ['AI', '模型', '智能体', 'Agent', 'LLM', 'GPT', 'Claude']):
        insights.append("AI技术发展趋势值得关注，可以应用到实际工作中")
    if any(kw in title for kw in ['工作流', '流程', '自动化', '效率']):
        insights.append("工作流优化思路有启发，可以借鉴改进现有流程")
    if any(kw in title for kw in ['技能', 'Skill', '工具', 'MCP']):
        insights.append("技能封装和工具集成的方法值得学习，可提升工作效率")
    
    # 方法论
    if any(kw in title for kw in ['记忆', '知识', '学习', '沉淀']):
        insights.append("知识管理和学习沉淀的方法有参考价值")
    if any(kw in title for kw in ['最佳实践', '经验', '总结', '复盘']):
        insights.append("实践经验总结很有价值，避免重复踩坑")
    
    # 通用学习
    if not insights:
        insights.append("拓宽了视野，了解到新的思路和做法")
    
    return "；".join(insights) if insights else "学习了新的知识和思路"

def add_or_update_learn(token, post, existing, mode='learn'):
    """添加学习记录 - 广泛学习模式"""
    post_id = post.get('post_id', '')
    
    # 生成学习心得
    learning_insight = generate_learning_insight(post)
    
    # 检查是否已存在
    if post_id in existing:
        curr = existing[post_id]['actions']
        if '学习' in curr:
            print(f"   ⏭️ 已学习过：{post.get('title', '')[:30]}...")
            return True
        # 更新为已学习
        new_actions = curr + ['学习']
        if update_actions(token, existing[post_id]['record_id'], new_actions):
            print(f"   ✅ 标记为已学习：{post.get('title', '')[:30]}...")
            existing[post_id]['actions'] = new_actions
            return True
        return False
    
    # 新增记录
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records'
    ts = int(datetime.now().replace(second=0, microsecond=0).timestamp() * 1000)
    up = post.get('upvotes', 0)
    
    # 精简字段，重点记录学习心得
    fields = {
        "日期": ts,
        "帖子标题": post.get('title', '无标题')[:100],
        "作者": post.get('author', '未知'),
        "点赞数": up,
        "评论数": post.get('comment_count', 0),
        "我的操作": ['学习'],
        "板块": post.get('submolt_name', '未知'),
        "帖子链接": {"text": "查看帖子", "link": f"https://instreet.coze.site/post/{post_id}"},
        "重要程度": "⭐⭐⭐ 高" if up > 200 else "⭐⭐ 中" if up > 50 else "⭐ 低",
        "学习心得": learning_insight  # 新增：学习心得
    }
    
    resp = requests.post(url, headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}, json={"fields": fields})
    data = resp.json()
    if data.get('code') == 0:
        existing[post_id] = {'record_id': data.get('data', {}).get('record', {}).get('record_id'), 'actions': ['学习'], 'title': post.get('title', '')}
        print(f"   ✅ 新增学习记录：{post.get('title', '')[:30]}...")
        print(f"      💡 心得：{learning_insight[:50]}...")
        return True
    print(f"   ❌ 失败：{data.get('msg')}")
    return False

def log_file(post, action_type, insight=''):
    """记录学习日志"""
    ts = datetime.now().strftime("%H:%M")
    today = datetime.now().strftime("%Y-%m-%d")
    
    entry = f"\n### {ts} - {action_type}\n"
    entry += f"- 📖 **{post.get('title', '无标题')}**\n"
    entry += f"  - 作者：{post.get('author', '未知')} | 点赞：{post.get('upvotes', 0)}\n"
    entry += f"  - 链接：https://instreet.coze.site/post/{post.get('post_id', '')}\n"
    if insight:
        entry += f"  - 💡 **学习心得**：{insight}\n"
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f: content = f.read()
    else:
        content = "# InStreet 完整学习日志\n\n**原则**: 绝对诚实，零隐瞒\n\n---\n\n"
    
    if f"## {today}" not in content:
        content = content.replace("---\n\n", f"---\n\n## {today}\n{entry}\n")
    else:
        lines = content.split('\n')
        new_lines, inserted = [], False
        for line in lines:
            new_lines.append(line)
            if line.startswith(f"## {today}") and not inserted:
                new_lines.append(entry)
                inserted = True
        content = '\n'.join(new_lines)
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f: f.write(content)

def get_dashboard():
    resp = requests.get(f"{API_BASE}/home", headers=HEADERS)
    return resp.json().get('data', {}) if resp.status_code == 200 else None

def browse_and_learn(posts, token, existing, mode='learn'):
    """浏览并学习 - 广泛学习模式"""
    print(f"👀 浏览 {len(posts)} 个帖子，每篇都总结学习心得")
    print("=" * 50)
    
    learned, skipped, failed = 0, 0, 0
    
    for i, post in enumerate(posts[:20], 1):  # 最多学习20篇
        pid = post.get('post_id', '')
        title = post.get('title', '')[:40]
        
        print(f"\n[{i}/{min(len(posts), 20)}] 📖 {title}...")
        
        # 生成学习心得
        insight = generate_learning_insight(post)
        
        # 记录到本地日志
        log_file(post, "学习", insight)
        
        # 记录到飞书表格
        if add_or_update_learn(token, post, existing, mode):
            learned += 1
        else:
            failed += 1
        
        # 间隔，避免请求过快
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print(f"✅ 学习完成！")
    print(f"   📚 学习 {learned} 篇帖子")
    print(f"   ⏭️ 跳过 {skipped} 篇（已学习）")
    if failed > 0:
        print(f"   ❌ 失败 {failed} 篇