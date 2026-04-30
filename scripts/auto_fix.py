#!/usr/bin/env python3
"""
自动修复常见错误
规则：遇到错误 → 能自动修复？→ 立即修复
"""

import os
import subprocess
import sys
from pathlib import Path

# 常见错误及修复方案
AUTO_FIX_RULES = {
    "ModuleNotFoundError": {
        "pattern": "No module named",
        "fix": "pip_install",
        "description": "Python模块缺失，自动安装"
    },
    "FileNotFoundError": {
        "pattern": "No such file or directory",
        "fix": "create_directory",
        "description": "文件或目录不存在，自动创建"
    },
    "PermissionError": {
        "pattern": "Permission denied",
        "fix": "chmod_fix",
        "description": "权限不足，自动修复权限"
    },
    "GitError": {
        "pattern": "not a git repository",
        "fix": "git_init",
        "description": "Git仓库未初始化"
    }
}

def pip_install(module_name):
    """自动安装Python模块"""
    try:
        subprocess.run(["pip3.10", "install", module_name, "-q"], check=True)
        return True, f"✓ 已自动安装模块: {module_name}"
    except Exception as e:
        return False, f"✗ 安装失败: {str(e)}"

def create_directory(path):
    """自动创建目录"""
    try:
        os.makedirs(path, exist_ok=True)
        return True, f"✓ 已自动创建目录: {path}"
    except Exception as e:
        return False, f"✗ 创建失败: {str(e)}"

def chmod_fix(path):
    """自动修复权限"""
    try:
        os.chmod(path, 0o755)
        return True, f"✓ 已自动修复权限: {path}"
    except Exception as e:
        return False, f"✗ 权限修复失败: {str(e)}"

def git_init():
    """自动初始化Git仓库"""
    try:
        subprocess.run(["git", "init"], check=True)
        return True, "✓ 已自动初始化Git仓库"
    except Exception as e:
        return False, f"✗ Git初始化失败: {str(e)}"

def try_auto_fix(error_message, context=None):
    """
    尝试自动修复错误
    
    Args:
        error_message: 错误信息
        context: 上下文信息（如文件路径等）
    
    Returns:
        (success, message): 是否修复成功及消息
    """
    for error_type, rule in AUTO_FIX_RULES.items():
        if rule["pattern"] in error_message:
            print(f"检测到可自动修复的错误类型: {error_type}")
            print(f"修复方案: {rule['description']}")
            
            # 执行修复
            if rule["fix"] == "pip_install":
                # 提取模块名
                if "No module named '" in error_message:
                    module = error_message.split("No module named '")[1].split("'")[0]
                    return pip_install(module)
            elif rule["fix"] == "create_directory":
                if context and "path" in context:
                    return create_directory(context["path"])
            elif rule["fix"] == "chmod_fix":
                if context and "path" in context:
                    return chmod_fix(context["path"])
            elif rule["fix"] == "git_init":
                return git_init()
    
    return False, "未找到自动修复方案"

if __name__ == "__main__":
    # 测试
    if len(sys.argv) > 1:
        error_msg = sys.argv[1]
        success, msg = try_auto_fix(error_msg)
        print(msg)
