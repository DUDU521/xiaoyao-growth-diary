# 网站配图索引

**更新日期**: 2026-03-22  
**生成工具**: ModelScope 文生图 Skill (Tongyi-MAI/Z-Image-Turbo)

---

## 📸 已生成的图片

### 1. 智能模型切换流程图
- **文件名**: `model_switching_flowchart.jpg`
- **用途**: 智能模型切换使用指南配图
- **提示词**: "智能模型切换流程图，科技感，蓝色调，AI模型图标"
- **关联文档**: `Smart_Model_Switching_Guide.md`

### 2. OpenClaw系统架构图  
- **文件名**: `openclaw_architecture.jpg`
- **用途**: OpenClaw架构分析文档配图
- **提示词**: "OpenClaw系统架构图，技术感，模块化设计，数据流向图"
- **关联文档**: `OpenClaw_Architecture_Analysis.md`

### 3. 智慧医院系统界面
- **文件名**: `smart_hospital_dashboard.jpg`
- **用途**: 智慧医院任务分配文档配图
- **提示词**: "智慧医院系统界面，现代化医疗，数据可视化大屏"
- **关联文档**: `Smart_Hospital_Task_Assignment.md`

### 4. 临床路径工作流程图
- **文件名**: `clinical_pathway_flow.jpg`
- **用途**: 临床路径需求和演示文档配图
- **提示词**: "临床路径工作流程图，医疗流程图，绿色健康色调"
- **关联文档**: `Clinical_Pathway_Requirements.md`, `Clinical_Pathway_Demo.md`

---

## 🎨 图片使用指南

### 在Markdown中引用

```markdown
![智能模型切换流程图](./images/model_switching_flowchart.jpg)
```

### 在HTML中引用

```html
<img src="./images/model_switching_flowchart.jpg" alt="智能模型切换流程图" />
```

---

## 🛠️ 生成新图片

使用文生图Skill生成新配图：

```bash
cd /home/admin/.openclaw/workspace/skills/modelscope-image-gen
python3 scripts/generate.py "你的图片描述" output_filename.jpg
```

生成的图片会自动保存在 `generated_images/` 目录。

---

## 📋 待生成的图片清单

- [ ] 互联网医院推广流程图
- [ ] 医疗闭环数据整改流程图
- [ ] 出院智能体工作界面
- [ ] 办公技能安装界面截图
- [ ] 技能清单总览图

---

**备注**: 所有图片均使用ModelScope API生成，支持中文提示词，生成时间约20-30秒/张。