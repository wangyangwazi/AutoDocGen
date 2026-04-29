# AutoDocGen (开源代码库全自动文档生成器)

![AutoDocGen](https://img.shields.io/badge/Powered%20by-LLM-blue?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge)

## 📖 项目简介

在现代软件开发中，维护高质量的文档往往被视为繁重且费时的任务。**AutoDocGen** 是一个开箱即用的开源工具，旨在彻底解决“代码无文档”、“旧项目难接手”的痛点。

本项目基于通用的大语言模型 (LLM) 架构设计，**全面兼容任何支持 OpenAI 接口格式的模型（如 OpenAI, Gemini, DeepSeek, MIMO 等）**。它能自动遍历本地代码库（如 Python, JS, Java, C++ 等），深入理解代码业务逻辑，并一键生成排版整洁、结构清晰的 Markdown 技术文档。

## ✨ 核心特性
- 🚀 **全自动解析**: 自动递归遍历指定目录，识别主流编程语言文件。
- 🧠 **深度代码理解**: 提取核心函数、类定义，并用自然语言解释其输入输出及业务逻辑。
- 🛡️ **轻量级架构**: 无需复杂的数据库，纯 Python 编写，极易进行二次开发。

## 🛠️ 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
复制 `.env.example` 文件并重命名为 `.env`，根据你使用的大模型厂商，填入对应的 API Key、Base URL 以及模型名称。

### 3. 运行测试
修改 `main.py` 中的 `TARGET_REPO` 为你想解析的本地代码库路径，然后运行：
```bash
python main.py
```
运行结束后，生成的技术文档将保存在 `docs_output/` 文件夹中。

## 🤝 贡献与开源
欢迎提交 Issue 和 Pull Request，让开发者们不再为写文档而脱发！
