# AutoDocGen (开源代码库全自动文档生成器)

![AutoDocGen](https://img.shields.io/badge/Powered%20by-LLM-blue?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge)

## 📖 项目简介

在现代软件开发中，维护高质量的文档往往被视为繁重且费时的任务。**AutoDocGen** 是一个开箱即用的开源工具，它旨在彻底解决“代码无文档”、“旧项目难接手”的痛点。

本项目通过接入主流的大语言模型 (LLM)，自动遍历本地代码库（如 Python, JS, Java, C++ 等），深入理解代码业务逻辑，并一键生成排版整洁、结构清晰的 Markdown 技术文档。

无论是企业内部的老旧代码，还是大型开源项目（如 Linux Kernel、Vue 源码），只要为其提供充足的 LLM Token，AutoDocGen 都能不知疲倦地为你梳理出清晰的知识库。

## ✨ 核心特性
- 🚀 **全自动解析**: 自动递归遍历指定目录，识别主流编程语言文件。
- 🧠 **深度代码理解**: 提取核心函数、类定义，并用自然语言解释其输入输出及业务逻辑。
- 📝 **标准化输出**: 生成的 Markdown 文件可直接发布到静态站点生成器（如 VitePress、Docusaurus）。
- 🛡️ **轻量级架构**: 无需复杂的数据库，纯 Python 编写，极易进行二次开发。

## 🛠️ 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
本项目支持任何兼容 OpenAI 接口格式的大模型。复制 `.env.example` 文件并重命名为 `.env`，填入你的 API Key、Base URL 以及模型名称：
```env
API_KEY=your_api_key_here
BASE_URL=https://api.your_provider.com/v1
MODEL_NAME=your_model_name
```

### 3. 运行测试
我们在 `test_repo/` 目录下准备了极简的测试代码。
```bash
python main.py
```
运行结束后，生成的技术文档将保存在 `docs_output/` 文件夹中。

## 🏗️ 进阶使用：解析大型项目 (高 Token 消耗预警)
修改 `main.py` 中的 `TARGET_REPO` 变量，将其指向你本地庞大的开源项目文件夹（例如 `D:/projects/vue-next`）。
由于大型项目包含成百上千个文件，需要大模型进行高频读取和超长上下文推理，**单次完整解析可能会消耗数十万甚至数百万的 Token**。在使用此功能解析巨型工程之前，请确保您的 API 账户有充足的额度。

## 🤝 贡献与开源
欢迎提交 Issue 和 Pull Request，让开发者们不再为写文档而脱发！
