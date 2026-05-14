<div align="center">

# 🎨 PromptCraft

**輕量級AI Prompt優化與管理工具**

*Lightweight AI Prompt Optimization & Management Tool*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

</div>

---

## 🎉 專案介紹

**PromptCraft** 是一個簡潔優雅的AI Prompt管理工具，幫助您組織、優化和複用高品質的AI提示詞。無論您是開發者、寫作者還是AI愛好者，PromptCraft都能讓您的AI互動更加高效。

**核心差異化亮點：**
- 🚀 **零依賴輕量**: 純Python實現，無需複雜環境配置
- 🔒 **本地優先**: SQLite本地儲存，資料完全私有化
- ✨ **智慧優化**: 內建Prompt品質分析與自動優化
- 🌐 **跨平臺**: Windows、macOS、Linux全平臺支援
- 📚 **多語言**: 繁體中文、簡體中文、英文完整文件

## ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 📚 **Prompt庫** | 建立、編輯、分類管理Prompt，支援標籤 |
| 🔍 **智慧搜尋** | 全文檢索所有Prompt內容 |
| ⭐ **收藏功能** | 快速訪問常用Prompt |
| 🎯 **Prompt優化器** | 一鍵優化，品質評分 |
| 🔧 **變數模板** | `{{variable}}` 佔位符動態替換 |
| 📊 **使用統計** | 追蹤Prompt使用資料 |
| 📤 **匯入匯出** | 支援JSON和Markdown格式 |

## 🚀 快速開始

### 安裝

```bash
# 從PyPI安裝（即將釋出）
pip install promptcraft

# 或從原始碼安裝
git clone https://github.com/gitstq/promptcraft.git
cd promptcraft
pip install -e .
```

### 基礎用法

```bash
# 初始化
promptcraft init

# 建立Prompt
promptcraft create "程式碼審查" "請審查這段程式碼: {{code}}" --category coding

# 列出所有Prompt
promptcraft list

# 使用Prompt（替換變數）
promptcraft use 1 --var code="def hello(): pass"

# 分析Prompt品質
promptcraft analyze 1

# 優化Prompt
promptcraft optimize 1 --save
```

## 📖 詳細使用指南

### 建立Prompt

```bash
# 基礎建立
promptcraft create "標題" "內容"

# 帶選項建立
promptcraft create "我的Prompt" "內容" \
  --description "描述資訊" \
  --category writing \
  --tags "創意,寫作" \
  --model gpt-4 \
  --favorite
```

### 管理Prompt

```bash
# 檢視詳情
promptcraft show 1

# 更新
promptcraft update 1 --title "新標題"

# 刪除
promptcraft delete 1

# 切換收藏
promptcraft favorite 1

# 複製
promptcraft duplicate 1
```

### 使用變數

建立帶變數的Prompt：
```
你好 {{name}}，歡迎來到 {{place}}！
```

使用時替換變數：
```bash
promptcraft use 1 --var name="張三" --var place="台北"
```

### 優化功能

PromptCraft從5個維度分析Prompt品質：
- **清晰度** (25%): 指令明確，無歧義
- **結構化** (25%): 格式規範，層次分明
- **上下文** (20%): 背景資訊充足
- **具體性** (15%): 包含示例和約束條件
- **長度適中** (15%): 不過短也不過長

```bash
# 分析品質
promptcraft analyze 1

# 優化並儲存
promptcraft optimize 1 --save
```

## 💡 設計思路

PromptCraft遵循以下設計理念：

1. **簡潔**: 學習成本低，命令直觀易懂
2. **隱私**: 無雲服務，資料完全本地儲存
3. **高效**: 鍵盤驅動的工作流，適合高階使用者
4. **可擴充套件**: 清晰的API設計，便於功能擴充套件

## 📦 從原始碼構建

```bash
# 克隆倉庫
git clone https://github.com/gitstq/promptcraft.git
cd promptcraft

# 安裝依賴
pip install -r requirements.txt

# 執行測試
pytest tests/ -v

# 構建包
python setup.py sdist bdist_wheel

# 構建可執行檔案（可選）
python scripts/build.py all
```

## 🤝 貢獻指南

歡迎提交Pull Request！

1. Fork本倉庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 新增某個功能'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 建立Pull Request

## 📄 開源協議

本專案採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 檔案。
