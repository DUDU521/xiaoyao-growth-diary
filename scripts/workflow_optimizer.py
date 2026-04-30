#!/usr/bin/env python3
"""
工作流优化
规则：
- 一次接收所有需求，不要来回确认
- 多个简单任务，一条消息完成
- 需要确认的，列出选项让用户选
- 模糊输入时，主动列出选项
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re

@dataclass
class UserRequest:
    """用户请求"""
    raw_input: str
    intent: str = ""
    entities: Dict[str, Any] = None
    confidence: float = 0.0
    needs_clarification: bool = False
    options: List[str] = None


class WorkflowOptimizer:
    """工作流优化器"""
    
    def __init__(self):
        # 常见意图模式
        self.intent_patterns = {
            "search": ["搜索", "查找", "找", "查", "看看"],
            "create": ["创建", "新建", "写", "生成", "做"],
            "update": ["更新", "修改", "改", "编辑"],
            "delete": ["删除", "移除", "去掉"],
            "analyze": ["分析", "统计", "计算", "评估"],
            "deploy": ["部署", "发布", "上线", "安装"],
            "query": ["查询", "查看", "显示", "列出"],
        }
        
        # 模糊输入的常见歧义
        self.ambiguous_terms = {
            "博客": ["写博客文章", "查看博客统计", "部署博客", "备份博客"],
            "文档": ["创建文档", "编辑文档", "查看文档", "删除文档"],
            "数据": ["分析数据", "导出数据", "导入数据", "清理数据"],
            "任务": ["创建任务", "查看任务", "完成任务", "删除任务"],
            "报告": ["生成报告", "查看报告", "导出报告", "打印报告"],
        }
    
    def parse_request(self, user_input: str) -> UserRequest:
        """
        解析用户请求
        
        Args:
            user_input: 用户原始输入
            
        Returns:
            UserRequest: 解析后的请求对象
        """
        request = UserRequest(raw_input=user_input)
        request.entities = {}
        
        # 1. 检测意图
        detected_intent = self._detect_intent(user_input)
        request.intent = detected_intent["intent"]
        request.confidence = detected_intent["confidence"]
        
        # 2. 提取实体
        request.entities = self._extract_entities(user_input)
        
        # 3. 检查是否需要澄清
        clarification = self._check_clarification(user_input)
        request.needs_clarification = clarification["needs_clarification"]
        request.options = clarification["options"]
        
        return request
    
    def _detect_intent(self, text: str) -> Dict[str, Any]:
        """检测用户意图"""
        text_lower = text.lower()
        
        for intent, keywords in self.intent_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return {
                        "intent": intent,
                        "confidence": 0.8
                    }
        
        return {
            "intent": "unknown",
            "confidence": 0.0
        }
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """提取实体信息"""
        entities = {}
        
        # 提取文件名
        file_pattern = r'[\w\-\.]+\.(md|txt|py|js|json|yaml|yml|docx|xlsx)'
        files = re.findall(file_pattern, text)
        if files:
            entities["files"] = files
        
        # 提取日期
        date_pattern = r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?'
        dates = re.findall(date_pattern, text)
        if dates:
            entities["dates"] = dates
        
        # 提取数字
        number_pattern = r'\d+'
        numbers = re.findall(number_pattern, text)
        if numbers:
            entities["numbers"] = [int(n) for n in numbers]
        
        return entities
    
    def _check_clarification(self, text: str) -> Dict[str, Any]:
        """检查是否需要澄清"""
        for term, options in self.ambiguous_terms.items():
            if term in text:
                return {
                    "needs_clarification": True,
                    "options": options
                }
        
        # 检查输入是否过于简短或模糊
        if len(text) < 5:
            return {
                "needs_clarification": True,
                "options": ["请提供更多详细信息"]
            }
        
        return {
            "needs_clarification": False,
            "options": []
        }
    
    def generate_response(self, request: UserRequest) -> str:
        """
        生成响应
        
        Args:
            request: 解析后的请求
            
        Returns:
            response: 响应文本
        """
        if request.needs_clarification:
            return self._generate_clarification_prompt(request)
        
        # 直接处理请求
        return f"收到您的请求：{request.raw_input}\n意图：{request.intent}\n实体：{request.entities}"
    
    def _generate_clarification_prompt(self, request: UserRequest) -> str:
        """生成澄清提示"""
        options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(request.options)])
        
        return f"""您的输入"{request.raw_input}"可能有多种理解，请确认您想要：

{options_text}

请回复数字（如：1）或具体描述您的需求。"""
    
    def batch_process(self, tasks: List[Dict[str, Any]]) -> List[str]:
        """
        批量处理多个简单任务
        
        Args:
            tasks: 任务列表，每个任务是{"name": str, "func": callable, "args": tuple}
            
        Returns:
            results: 结果列表
        """
        results = []
        print(f"[工作流优化] 批量处理 {len(tasks)} 个任务")
        
        for i, task in enumerate(tasks, 1):
            print(f"[工作流优化] 任务 {i}/{len(tasks)}: {task['name']}")
            try:
                result = task["func"](*task.get("args", ()))
                results.append(f"✓ {task['name']}: 完成")
            except Exception as e:
                results.append(f"✗ {task['name']}: 失败 - {str(e)}")
        
        return results
    
    def suggest_options(self, context: str, available_actions: List[str]) -> str:
        """
        根据上下文建议选项
        
        Args:
            context: 当前上下文
            available_actions: 可用操作列表
            
        Returns:
            suggestion: 建议文本
        """
        options_text = "\n".join([f"• {action}" for action in available_actions])
        
        return f"""根据您提到的"{context}"，您可以：

{options_text}

请告诉我您想要执行哪个操作。"""


# 使用示例
def example_task_1():
    """示例任务1"""
    return "任务1结果"

def example_task_2():
    """示例任务2"""
    return "任务2结果"


if __name__ == "__main__":
    optimizer = WorkflowOptimizer()
    
    # 示例1：解析模糊输入
    print("=== 示例1：解析模糊输入 ===")
    test_inputs = [
        "博客",
        "帮我处理一下数据",
        "创建文档",
        "部署",
    ]
    
    for user_input in test_inputs:
        print(f"\n用户输入: {user_input}")
        request = optimizer.parse_request(user_input)
        response = optimizer.generate_response(request)
        print(response)
    
    # 示例2：批量处理
    print("\n=== 示例2：批量处理 ===")
    tasks = [
        {"name": "任务A", "func": example_task_1},
        {"name": "任务B", "func": example_task_2},
        {"name": "任务C", "func": example_task_1},
    ]
    results = optimizer.batch_process(tasks)
    print("\n".join(results))
