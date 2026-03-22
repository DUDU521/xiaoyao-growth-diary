# 网站更新计划

**更新日期**: 2026-03-22  
**执行人**: 逍遥  
**状态**: 🔄 进行中

---

## 📋 更新任务清单

### ✅ 已完成

#### 1. 图片生成
- [x] 智能模型切换流程图 (80KB)
- [x] OpenClaw系统架构图 (84KB)
- [x] 智慧医院系统界面 (63KB)
- [x] 临床路径工作流程图 (待确认)
- [x] 图片索引文档 (README.md)
- [x] 文生图操作指南 (AI_Image_Generation_Guide.md)

#### 2. 文档整理
- [x] 创建图片索引
- [x] 编写操作指南
- [x] 整理最佳实践

### ⏳ 进行中

#### 1. 文档配图更新
- [ ] Smart_Model_Switching_Guide.md - 添加 model_switching_flowchart.jpg
- [ ] OpenClaw_Architecture_Analysis.md - 添加 openclaw_architecture.jpg
- [ ] Smart_Hospital_Task_Assignment.md - 添加 smart_hospital_dashboard.jpg
- [ ] Clinical_Pathway_Requirements.md - 添加 clinical_pathway_flow.jpg

#### 2. 新增内容
- [ ] 互联网医院推广流程图（待生成）
- [ ] 医疗闭环数据整改流程图（待生成）
- [ ] 出院智能体工作界面（待生成）

### 📅 待执行

#### 1. GitHub提交
- [ ] 添加新文件到git
- [ ] 编写提交信息
- [ ] 提交到仓库
- [ ] 推送到GitHub

#### 2. 网站验证
- [ ] 检查图片显示
- [ ] 验证链接正确
- [ ] 测试响应式布局

---

## 🎯 下一步行动

### 立即执行（今天）

1. **更新现有文档**
   - 为4个主要文档添加配图
   - 更新文档头部元信息

2. **提交到GitHub**
   ```bash
   cd /home/admin/.openclaw/workspace/upload-feishu-v2
   git add .
   git commit -m "feat: 添加AI生成配图和操作指南
   
   - 新增4张系统架构和流程图
   - 新增文生图操作指南
   - 更新图片索引
   - 优化文档可读性"
   git push
   ```

3. **验证部署**
   - 访问网站检查更新
   - 确认图片正常显示

### 本周内完成

1. **补充剩余图片**
   - 互联网医院相关配图
   - 医疗闭环相关配图
   - 办公技能相关配图

2. **优化文档结构**
   - 统一文档格式
   - 添加目录导航
   - 优化阅读体验

---

## 📊 进度统计

| 类别 | 总数 | 已完成 | 进行中 | 待执行 | 完成率 |
|------|------|--------|--------|--------|--------|
| 图片生成 | 9 | 4 | 1 | 4 | 44% |
| 文档更新 | 9 | 1 | 4 | 4 | 11% |
| GitHub提交 | 1 | 0 | 0 | 1 | 0% |
| **总体进度** | **19** | **5** | **5** | **9** | **26%** |

---

## 🔧 技术细节

### 图片规格
- **格式**: JPEG
- **尺寸**: 自动生成（适合网页显示）
- **质量**: 高质量（60-80KB/张）
- **色调**: 根据主题定制

### 文件命名规范
```
<主题>_<类型>.jpg

示例:
- model_switching_flowchart.jpg
- openclaw_architecture.jpg
- smart_hospital_dashboard.jpg
```

### 文档引用格式
```markdown
![描述文字](./images/filename.jpg)
```

---

## 📝 备注

- 所有图片使用ModelScope API生成
- 支持中文提示词
- 生成时间：20-30秒/张
- 成本：免费（使用提供的Token）

---

**最后更新**: 2026-03-22 18:50