#!/bin/bash

# 逍遥的成长日记 - 部署脚本
# 用于将网站部署到 GitHub Pages

echo "🚀 开始部署逍遥的成长日记网站..."

# 检查是否在正确的目录
if [ ! -f "index.html" ]; then
    echo "❌ 错误: 当前目录不是网站根目录"
    exit 1
fi

# 创建备份
echo "💾 创建备份..."
cp -r . ../xiaoyao-growth-diary-website-backup-$(date +%Y%m%d-%H%M%S)

# 初始化 git 仓库（如果不存在）
if [ ! -d ".git" ]; then
    echo "🔧 初始化 Git 仓库..."
    git init
    git remote add origin https://github.com/DUDU521/xiaoyao-growth-diary.git
fi

# 添加所有文件
echo "📂 添加文件到 Git..."
git add .

# 提交更改
echo "📝 提交更改..."
git commit -m "Update website - $(date '+%Y-%m-%d %H:%M:%S')"

# 推送到 GitHub
echo "📤 推送到 GitHub..."
git push origin main

echo "✅ 部署完成！网站已更新到 GitHub Pages"
echo "🌐 访问地址: https://dudu521.github.io/xiaoyao-growth-diary/"