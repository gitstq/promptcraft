# PromptCraft - 轻量级AI Prompt优化与管理工具

## 🎯 项目定位
一个简洁优雅的AI Prompt管理工具，帮助用户组织、优化和复用高质量的AI提示词。

## 📋 核心功能

### 1. Prompt库管理
- 创建、编辑、分类Prompt
- 标签系统（多维度分类）
- 收藏/常用Prompt快速访问
- 导入/导出功能（JSON/Markdown）

### 2. Prompt优化器
- 一键优化Prompt（清晰度、结构化、上下文）
- Prompt质量评分
- 优化建议与改进历史

### 3. 变量模板系统
- 支持 {{variable}} 变量占位符
- 快速填充表单生成最终Prompt
- 常用变量预设

### 4. 多模型适配
- 支持 Claude、GPT、Gemini 等主流模型
- 模型特定的Prompt格式建议
- Token预估

### 5. 快捷操作
- 命令行快速调用
- 剪贴板集成
- 快捷键支持

## 🛠️ 技术栈
- **语言**: Python 3.9+
- **CLI框架**: Click / Rich
- **数据存储**: SQLite (本地)
- **配置**: YAML/JSON
- **打包**: PyInstaller (可执行文件)

## 📁 项目结构
```
promptcraft/
├── promptcraft/          # 主包
│   ├── __init__.py
│   ├── cli.py           # 命令行接口
│   ├── core.py          # 核心业务逻辑
│   ├── optimizer.py     # Prompt优化引擎
│   ├── storage.py       # 数据存储层
│   ├── templates.py     # 模板系统
│   └── utils.py         # 工具函数
├── tests/               # 测试
├── docs/                # 文档
├── scripts/             # 构建脚本
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## 🎨 差异化亮点
1. **零依赖轻量**: 纯Python实现，无需复杂环境
2. **本地优先**: 数据本地存储，隐私安全
3. **智能优化**: 内置Prompt优化算法
4. **跨平台**: Windows/macOS/Linux全支持
5. **多语言文档**: 中英繁三语支持
