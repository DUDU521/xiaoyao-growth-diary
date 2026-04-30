#!/usr/bin/env python3
"""
上下文预加载
规则：根据消息预读内容，减少等待时间
"""

import re
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PreloadRule:
    """预加载规则"""
    keywords: List[str]
    files_to_load: List[str]
    description: str


class ContextPreloader:
    """上下文预加载器"""
    
    def __init__(self, workspace_path: str = "~/.openclaw/workspace"):
        """
        初始化预加载器
        
        Args:
            workspace_path: 工作区路径
        """
        self.workspace = Path(workspace_path).expanduser()
        self.preload_rules: List[PreloadRule] = []
        self.preloaded_context: Dict[str, Any] = {}
        self._init_rules()
    
    def _init_rules(self):
        """初始化预加载规则"""
        self.preload_rules = [
            PreloadRule(
                keywords=["博客", "blog", "文章", "article"],
                files_to_load=[
                    "memory/blog_config.json",
                    "memory/blog_posts.json",
                    "tools/blog_manager.py"
                ],
                description="博客相关操作"
            ),
            PreloadRule(
                keywords=["部署", "deploy", "发布", "上线", "install"],
                files_to_load=[
                    "scripts/deploy.sh",
                    ".env.deploy",
                    "config/deployment.yaml"
                ],
                description="部署相关操作"
            ),
            PreloadRule(
                keywords=["飞书", "feishu", "lark", "文档", "doc"],
                files_to_load=[
                    ".env.feishu",
                    "scripts/feishu_docs.py",
                    "memory/feishu_config.json"
                ],
                description="飞书文档操作"
            ),
            PreloadRule(
                keywords=["技能", "skill", "安装", "install"],
                files_to_load=[
                    "skills/",
                    "scripts/check_skills.py",
                    "memory/skills_registry.json"
                ],
                description="技能管理"
            ),
            PreloadRule(
                keywords=["记忆", "memory", "记录", "log"],
                files_to_load=[
                    "MEMORY.md",
                    "memory/",
                    "scripts/auto_memory_update.py"
                ],
                description="记忆管理"
            ),
            PreloadRule(
                keywords=["Git", "git", "提交", "commit", "push"],
                files_to_load=[
                    ".git/config",
                    ".gitignore",
                    "scripts/git_auto_commit.py"
                ],
                description="Git操作"
            ),
            PreloadRule(
                keywords=["任务", "task", "计划", "schedule", "cron"],
                files_to_load=[
                    "cron/",
                    "scripts/task_scheduler.py",
                    "memory/tasks.json"
                ],
                description="任务调度"
            ),
            PreloadRule(
                keywords=["患者", "医院", "门诊", "医疗", "hospital", "patient"],
                files_to_load=[
                    "memory/hospital_config.json",
                    "projects/hospital/",
                    "scripts/hospital_*.py"
                ],
                description="医疗项目"
            ),
            PreloadRule(
                keywords=["报告", "report", "汇报", "总结", "summary"],
                files_to_load=[
                    "reports/",
                    "memory/report_templates/",
                    "scripts/generate_report.py"
                ],
                description="报告生成"
            ),
            PreloadRule(
                keywords=["配置", "config", "设置", "setting"],
                files_to_load=[
                    ".config/",
                    ".env.*",
                    "config/"
                ],
                description="配置管理"
            ),
        ]
    
    def analyze_message(self, message: str) -> List[PreloadRule]:
        """
        分析消息，确定需要预加载的内容
        
        Args:
            message: 用户消息
            
        Returns:
            matched_rules: 匹配的规则列表
        """
        matched_rules = []
        message_lower = message.lower()
        
        for rule in self.preload_rules:
            for keyword in rule.keywords:
                if keyword.lower() in message_lower:
                    matched_rules.append(rule)
                    break
        
        return matched_rules
    
    def preload_context(self, message: str) -> Dict[str, Any]:
        """
        预加载上下文
        
        Args:
            message: 用户消息
            
        Returns:
            context: 预加载的上下文
        """
        matched_rules = self.analyze_message(message)
        context = {
            "matched_rules": [r.description for r in matched_rules],
            "preloaded_files": [],
            "errors": []
        }
        
        if not matched_rules:
            return context
        
        print(f"[上下文预加载] 检测到 {len(matched_rules)} 个相关规则")
        
        for rule in matched_rules:
            print(f"[上下文预加载] 预加载: {rule.description}")
            
            for file_pattern in rule.files_to_load:
                try:
                    files = self._resolve_pattern(file_pattern)
                    for file_path in files:
                        if file_path.exists():
                            content = self._load_file(file_path)
                            context["preloaded_files"].append({
                                "path": str(file_path),
                                "content": content,
                                "type": self._get_file_type(file_path)
                            })
                            print(f"[上下文预加载] ✓ 已加载: {file_path}")
                        else:
                            context["errors"].append(f"文件不存在: {file_path}")
                            
                except Exception as e:
                    context["errors"].append(f"加载失败 {file_pattern}: {str(e)}")
        
        self.preloaded_context = context
        return context
    
    def _resolve_pattern(self, pattern: str) -> List[Path]:
        """解析文件模式"""
        full_path = self.workspace / pattern
        
        if "*" in pattern:
            # 通配符模式
            return list(self.workspace.glob(pattern))
        elif full_path.is_dir():
            # 目录
            return [full_path]
        else:
            # 单个文件
            return [full_path]
    
    def _load_file(self, file_path: Path) -> str:
        """加载文件内容"""
        if file_path.is_dir():
            # 目录，返回文件列表
            files = list(file_path.iterdir())
            return f"目录包含 {len(files)} 个文件/子目录"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 限制内容长度
                if len(content) > 5000:
                    content = content[:5000] + "...\n[内容已截断]"
                return content
        except Exception as e:
            return f"[无法读取文件: {str(e)}]"
    
    def _get_file_type(self, file_path: Path) -> str:
        """获取文件类型"""
        if file_path.is_dir():
            return "directory"
        
        suffix = file_path.suffix.lower()
        type_map = {
            ".md": "markdown",
            ".py": "python",
            ".js": "javascript",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".sh": "shell",
            ".txt": "text",
            ".env": "env",
        }
        return type_map.get(suffix, "unknown")
    
    def get_preloaded_summary(self) -> str:
        """获取预加载内容摘要"""
        if not self.preloaded_context:
            return "未预加载任何内容"
        
        rules = self.preloaded_context.get("matched_rules", [])
        files = self.preloaded_context.get("preloaded_files", [])
        errors = self.preloaded_context.get("errors", [])
        
        summary = f"""[上下文预加载摘要]
• 匹配规则: {len(rules)} 个
• 预加载文件: {len(files)} 个
• 错误: {len(errors)} 个

匹配的规则:
"""
        for rule in rules:
            summary += f"  - {rule}\n"
        
        if files:
            summary += "\n预加载的文件:\n"
            for f in files[:5]:  # 只显示前5个
                summary += f"  - {f['path']} ({f['type']})\n"
            if len(files) > 5:
                summary += f"  ... 还有 {len(files) - 5} 个文件\n"
        
        return summary
    
    def suggest_context(self, message: str) -> str:
        """
        根据消息建议预加载的上下文
        
        Args:
            message: 用户消息
            
        Returns:
            suggestion: 建议文本
        """
        matched_rules = self.analyze_message(message)
        
        if not matched_rules:
            return "未检测到需要预加载的上下文"
        
        suggestions = []
        for rule in matched_rules:
            files = ", ".join([f"`{f}`" for f in rule.files_to_load[:3]])
            suggestions.append(f"• **{rule.description}**: 将预加载 {files}")
        
        return "\n".join(suggestions)


# 使用示例
if __name__ == "__main__":
    preloader = ContextPreloader()
    
    # 测试消息
    test_messages = [
        "帮我部署一下博客",
        "更新飞书文档",
        "检查一下技能状态",
        "查看今天的记忆",
        "提交Git更改",
        "生成患者服务平台的报告",
    ]
    
    for message in test_messages:
        print(f"\n{'='*60}")
        print(f"测试消息: {message}")
        print('='*60)
        
        # 显示建议
        suggestion = preloader.suggest_context(message)
        print(f"\n{suggestion}")
        
        # 预加载上下文
        context = preloader.preload_context(message)
        print(f"\n{preloader.get_preloaded_summary()}")
