# AutoDocGen (开源代码库全自动文档生成器)

![AutoDocGen](https://img.shields.io/badge/Powered%20by-LLM-blue?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge) ![UI](https://img.shields.io/badge/UI-Dark%20Mode-black?style=for-the-badge)

## 📖 项目简介

在现代软件开发中，维护高质量的文档往往被视为繁重且费时的任务。**AutoDocGen** 是一个开箱即用的开源效率工具，旨在彻底解决“代码无文档”、“旧项目难接手”的痛点。

本项目基于通用的大语言模型 (LLM) 架构设计，**全面兼容任何支持 OpenAI 接口格式的模型（如 OpenAI, Gemini, DeepSeek, MIMO 等）**。它能自动遍历本地代码库，深入理解代码业务逻辑，并**一键生成沉浸式、极客风的单页交互式 HTML 分析报告**，让你无需在众多 Markdown 文件中切来切去，即可总览全局。

## ✨ 核心特性
- 🚀 **一键弹窗解析**: 运行脚本即弹出系统原生的文件夹选择器，告别繁琐的路径硬编码。
- 🖥️ **沉浸式交互 UI**: 抛弃零散的 `.md` 碎文件，全景化输出独立的 `AutoDocGen_Report.html` 报告页面。自带侧边栏无刷新切换、暗黑模式美学与高级排版。
- 🌈 **原生代码高亮**: 最终的分析报告内置 `highlight.js` 与 `marked.js`，代码片段享受 VS Code 级别的语法高亮。
- 🌍 **万能 API 兼容**: 采用通用 OpenAI 兼容层协议，支持无缝切换你喜欢的任意大模型。
- 🛡️ **轻量级架构**: 纯 Python 编写，无需配置复杂的数据库或静态博客生成器，即开即用。

## 🛠️ 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
复制 `.env.example` 文件并重命名为 `.env`，根据你使用的大模型厂商，填入对应的 API Key、Base URL 以及模型名称：
```env
# 你的 API 密钥
API_KEY=your_api_key_here

# OpenAI 兼容格式的接口地址
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# 调用的模型名称
MODEL_NAME=gemini-1.5-pro
```

### 3. 运行体验
```bash
python main.py
```
运行后：
1. 屏幕会弹出一个目录选择器，请选择你想解析的代码文件夹。
2. 脚本会自动过滤掉 `.git`, `node_modules` 等无关文件夹，向大模型发送解析请求。
3. 运行结束后，请在根目录双击打开 **`AutoDocGen_Report.html`**
## 🤝 贡献与开源
欢迎提交 Issue 和 Pull Request，让开发者们不再为看祖传代码而脱发！
