#!/bin/bash
# AI&医疗信息化每日新闻推送脚本
# 搜索三类新闻并保存为文件，然后通过 message 通知用户

cd /home/admin/.openclaw/workspace

echo "=== 开始搜索新闻 ==="
# 搜索AI新闻
AI_NEWS=$(curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"${TAVILY_API_KEY}\",\"query\":\"AI 人工智能 最新新闻\",\"max_results\":10,\"search_depth\":\"basic\"}" 2>/dev/null)

echo "AI搜索完成"
