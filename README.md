<div align="center">

# 🎨 PromptCraft

**轻量级AI Prompt优化与管理工具**

*Lightweight AI Prompt Optimization & Management Tool*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

**PromptCraft** is a lightweight, elegant AI Prompt management tool that helps you organize, optimize, and reuse high-quality AI prompts. Whether you're a developer, writer, or AI enthusiast, PromptCraft makes your AI interactions more efficient.

**Key Differentiators:**
- 🚀 **Zero-dependency lightweight**: Pure Python implementation, no complex environment setup
- 🔒 **Privacy-first**: Local SQLite storage, your data stays on your device
- ✨ **Smart optimization**: Built-in prompt quality analysis and auto-optimization
- 🌐 **Cross-platform**: Full support for Windows, macOS, and Linux
- 📚 **Multilingual**: English, Simplified Chinese, and Traditional Chinese documentation

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📚 **Prompt Library** | Create, edit, and categorize prompts with tags |
| 🔍 **Smart Search** | Full-text search across all prompts |
| ⭐ **Favorites** | Quick access to frequently used prompts |
| 🎯 **Prompt Optimizer** | One-click optimization with quality scoring |
| 🔧 **Variable Templates** | Dynamic prompts with `{{variable}}` placeholders |
| 📊 **Usage Analytics** | Track prompt usage statistics |
| 📤 **Import/Export** | JSON and Markdown format support |

### 🚀 Quick Start

#### Installation

```bash
# Install from PyPI (coming soon)
pip install promptcraft

# Or install from source
git clone https://github.com/gitstq/promptcraft.git
cd promptcraft
pip install -e .
```

#### Basic Usage

```bash
# Initialize
promptcraft init

# Create a new prompt
promptcraft create "Code Reviewer" "Please review this code: {{code}}" --category coding

# List all prompts
promptcraft list

# Use a prompt
promptcraft use 1 --var code="def hello(): pass"

# Analyze prompt quality
promptcraft analyze 1

# Optimize a prompt
promptcraft optimize 1 --save
```

### 📖 Detailed Usage

#### Creating Prompts

```bash
# Basic creation
promptcraft create "Title" "Content"

# With options
promptcraft create "My Prompt" "Content here" \
  --description "A helpful prompt" \
  --category writing \
  --tags "creative,writing" \
  --model gpt-4 \
  --favorite
```

#### Managing Prompts

```bash
# Show prompt details
promptcraft show 1

# Update a prompt
promptcraft update 1 --title "New Title"

# Delete a prompt
promptcraft delete 1

# Toggle favorite
promptcraft favorite 1

# Duplicate a prompt
promptcraft duplicate 1
```

#### Using Variables

Create prompts with variables:
```
Hello {{name}}, welcome to {{place}}!
```

Use with variable substitution:
```bash
promptcraft use 1 --var name="Alice" --var place="Wonderland"
```

#### Optimization

PromptCraft analyzes your prompts across 5 dimensions:
- **Clarity** (25%): Clear instructions without ambiguity
- **Structure** (25%): Well-organized with proper formatting
- **Context** (20%): Sufficient background information
- **Specificity** (15%): Concrete examples and constraints
- **Length** (15%): Appropriate length (not too short or long)

```bash
# Analyze quality
promptcraft analyze 1

# Optimize and save
promptcraft optimize 1 --save
```

### 💡 Design Philosophy

PromptCraft was designed with these principles:

1. **Simplicity**: Minimal learning curve, intuitive commands
2. **Privacy**: No cloud services, everything stays local
3. **Efficiency**: Keyboard-driven workflow for power users
4. **Extensibility**: Clean API for future enhancements

### 📦 Building from Source

```bash
# Clone repository
git clone https://github.com/gitstq/promptcraft.git
cd promptcraft

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Build package
python setup.py sdist bdist_wheel

# Build executable (optional)
python scripts/build.py all
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**PromptCraft** 是一个简洁优雅的AI Prompt管理工具，帮助您组织、优化和复用高质量的AI提示词。无论您是开发者、写作者还是AI爱好者，PromptCraft都能让您的AI交互更加高效。

**核心差异化亮点：**
- 🚀 **零依赖轻量**: 纯Python实现，无需复杂环境配置
- 🔒 **本地优先**: SQLite本地存储，数据完全私有化
- ✨ **智能优化**: 内置Prompt质量分析与自动优化
- 🌐 **跨平台**: Windows、macOS、Linux全平台支持
- 📚 **多语言**: 简体中文、繁体中文、英文完整文档

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 📚 **Prompt库** | 创建、编辑、分类管理Prompt，支持标签 |
| 🔍 **智能搜索** | 全文检索所有Prompt内容 |
| ⭐ **收藏功能** | 快速访问常用Prompt |
| 🎯 **Prompt优化器** | 一键优化，质量评分 |
| 🔧 **变量模板** | `{{variable}}` 占位符动态替换 |
| 📊 **使用统计** | 追踪Prompt使用数据 |
| 📤 **导入导出** | 支持JSON和Markdown格式 |

### 🚀 快速开始

#### 安装

```bash
# 从PyPI安装（即将发布）
pip install promptcraft

# 或从源码安装
git clone https://github.com/gitstq/promptcraft.git
cd promptcraft
pip install -e .
```

#### 基础用法

```bash
# 初始化
promptcraft init

# 创建Prompt
promptcraft create "代码审查" "请审查这段代码: {{code}}" --category coding

# 列出所有Prompt
promptcraft list

# 使用Prompt（替换变量）
promptcraft use 1 --var code="def hello(): pass"

# 分析Prompt质量
promptcraft analyze 1

# 优化Prompt
promptcraft optimize 1 --save
```

### 📖 详细使用指南

#### 创建Prompt

```bash
# 基础创建
promptcraft create "标题" "内容"

# 带选项创建
promptcraft create "我的Prompt" "内容" \
  --description "描述信息" \
  --category writing \
  --tags "创意,写作" \
  --model gpt-4 \
  --favorite
```

#### 管理Prompt

```bash
# 查看详情
promptcraft show 1

# 更新
promptcraft update 1 --title "新标题"

# 删除
promptcraft delete 1

# 切换收藏
promptcraft favorite 1

# 复制
promptcraft duplicate 1
```

#### 使用变量

创建带变量的Prompt：
```
你好 {{name}}，欢迎来到 {{place}}！
```

使用时替换变量：
```bash
promptcraft use 1 --var name="张三" --var place="北京"
```

#### 优化功能

PromptCraft从5个维度分析Prompt质量：
- **清晰度** (25%): 指令明确，无歧义
- **结构化** (25%): 格式规范，层次分明
- **上下文** (20%): 背景信息充足
- **具体性** (15%): 包含示例和约束条件
- **长度适中** (15%): 不过短也不过长

```bash
# 分析质量
promptcraft analyze 1

# 优化并保存
promptcraft optimize 1 --save
```

### 💡 设计思路

PromptCraft遵循以下设计理念：

1. **简洁**: 学习成本低，命令直观易懂
2. **隐私**: 无云服务，数据完全本地存储
3. **高效**: 键盘驱动的工作流，适合高级用户
4. **可扩展**: 清晰的API设计，便于功能扩展

### 📦 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/promptcraft.git
cd promptcraft

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/ -v

# 构建包
python setup.py sdist bdist_wheel

# 构建可执行文件（可选）
python scripts/build.py all
```

### 🤝 贡献指南

欢迎提交Pull Request！

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个功能'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🇹