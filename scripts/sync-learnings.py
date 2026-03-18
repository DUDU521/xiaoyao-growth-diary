#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
逍遥成长日记 - 学习记录同步脚本
自动将本地的学习记录同步到GitHub项目中
'''

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# 配置路径
LOCAL_LEARNINGS_DIR = '/home/admin/.openclaw/workspace/.learnings'
LOCAL_MEMORY_DIR = '/home/admin/.openclaw/workspace/.memory' 
PROJECT_DOCS_DIR = '/home/admin/.openclaw/workspace/projects/xiaoyao-growth-diary/docs'

def read_file_safe(filepath):
    '''安全读取文件内容'''
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f'读取文件失败 {filepath}: {e}')
        return None

def ensure_dir(directory):
    '''确保目录存在'''
    Path(directory).mkdir(parents=True, exist_ok=True)

def convert_learnings_to_markdown():
    '''转换学习记录为Markdown格式'''
    # 处理LEARNINGS.md
    learnings_file = os.path.join(LOCAL_LEARNINGS_DIR, 'LEARNINGS.md')
    if os.path.exists(learnings_file):
        content = read_file_safe(learnings_file)
        if content:
            # 创建最新经验目录
            latest_dir = os.path.join(PROJECT_DOCS_DIR, 'latest')
            ensure_dir(latest_dir)
            
            # 保存为最新经验
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            output_file = os.path.join(latest_dir, f'learnings-{timestamp}.md')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f'''---
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [automation, learning, ai]
category: methodology
---

# 自动学习记录 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{content}
''')
            print(f'已同步学习记录: {output_file}')

def convert_errors_to_pitfalls():
    '''转换错误记录为踩坑记录'''
    errors_file = os.path.join(LOCAL_LEARNINGS_DIR, 'ERRORS.md')
    if os.path.exists(errors_file):
        content = read_file_safe(errors_file)
        if content:
            pitfalls_dir = os.path.join(PROJECT_DOCS_DIR, 'categories', 'pitfalls')
            ensure_dir(pitfalls_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            output_file = os.path.join(pitfalls_dir, f'errors-{timestamp}.md')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f'''---
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [debugging, errors, troubleshooting]
category: pitfalls
---

# 错误记录分析 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{content}
''')
            print(f'已同步错误记录: {output_file}')

def sync_memory_facts():
    '''同步记忆事实'''
    facts_file = os.path.join(LOCAL_MEMORY_DIR, 'facts.md')
    if os.path.exists(facts_file):
        content = read_file_safe(facts_file)
        if content:
            memory_dir = os.path.join(PROJECT_DOCS_DIR, 'categories', 'cognition')
            ensure_dir(memory_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            output_file = os.path.join(memory_dir, f'memory-{timestamp}.md')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f'''---
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [memory, cognition, knowledge]
category: cognition
---

# 记忆事实更新 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{content}
''')
            print(f'已同步记忆事实: {output_file}')

def main():
    '''主函数'''
    print('开始同步逍遥成长日记内容...')
    
    # 确保项目目录结构
    categories = ['pitfalls', 'methodology', 'tools', 'inspiration', 'cognition', 'xiaoyao-diary']
    for category in categories:
        ensure_dir(os.path.join(PROJECT_DOCS_DIR, 'categories', category))
    
    # 执行同步
    convert_learnings_to_markdown()
    convert_errors_to_pitfalls() 
    sync_memory_facts()
    
    print('同步完成！')

if __name__ == '__main__':
    main()