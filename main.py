import os
import time
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from openai import OpenAI
from colorama import init, Fore, Style

# 初始化 colorama
init(autoreset=True)

# 载入环境变量
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

if not API_KEY or API_KEY == "your_api_key_here":
    print(Fore.RED + "❌ 错误: 请先在项目根目录创建 .env 文件，并配置 API_KEY")
    exit(1)

# 初始化客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# ========================
# 配置区
# ========================
OUTPUT_HTML_FILE = "AutoDocGen_Report.html"
SUPPORTED_EXTENSIONS = ['.py', '.js', '.java', '.cpp', '.c', '.go', '.ts', '.html', '.css', '.vue']

# ========================
# 现代美学 HTML/UI 模板
# ========================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoDocGen - 项目知识库</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark-reasonable.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        :root {{
            --bg-color: #0f172a;
            --sidebar-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --border-color: #334155;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}
        .sidebar {{
            width: 320px;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            box-shadow: 2px 0 10px rgba(0,0,0,0.3);
            z-index: 10;
        }}
        .sidebar-header {{
            padding: 24px;
            border-bottom: 1px solid var(--border-color);
            background: linear-gradient(135deg, #1e293b, #0f172a);
        }}
        .sidebar-header h1 {{
            font-size: 1.4rem;
            font-weight: 700;
            background: -webkit-linear-gradient(45deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 4px;
        }}
        .sidebar-header p {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        .file-list {{
            flex: 1;
            overflow-y: auto;
            padding: 12px;
        }}
        .file-item {{
            padding: 12px 16px;
            margin-bottom: 4px;
            border-radius: 8px;
            cursor: pointer;
            color: var(--text-muted);
            font-size: 0.9rem;
            transition: all 0.2s ease;
            word-break: break-all;
        }}
        .file-item:hover {{
            background-color: rgba(59, 130, 246, 0.1);
            color: var(--text-main);
            transform: translateX(4px);
        }}
        .file-item.active {{
            background-color: var(--accent);
            color: #fff;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }}
        .content-area {{
            flex: 1;
            overflow-y: auto;
            padding: 40px 60px;
            background: radial-gradient(circle at top right, #1e293b 0%, var(--bg-color) 60%);
        }}
        .markdown-body {{
            max-width: 900px;
            margin: 0 auto;
            line-height: 1.7;
            font-size: 1.05rem;
        }}
        .markdown-body h1, .markdown-body h2, .markdown-body h3 {{
            color: #fff;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: 600;
        }}
        .markdown-body h1 {{ font-size: 2.4rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3em; }}
        .markdown-body h2 {{ font-size: 1.8rem; color: #e2e8f0; }}
        .markdown-body p {{ margin-bottom: 1.2em; color: #cbd5e1; }}
        .markdown-body pre {{
            background-color: #0d1117;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            overflow-x: auto;
            margin: 1.5em 0;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
        }}
        .markdown-body code {{
            font-family: 'Fira Code', Consolas, Monaco, monospace;
            font-size: 0.9em;
        }}
        .markdown-body p code, .markdown-body li code {{
            background-color: rgba(59, 130, 246, 0.15);
            padding: 0.2em 0.4em;
            border-radius: 4px;
            color: #93c5fd;
        }}
        .markdown-body ul, .markdown-body ol {{ padding-left: 2em; margin-bottom: 1.2em; color: #cbd5e1; }}
        .markdown-body li {{ margin-bottom: 0.5em; }}
        .markdown-body blockquote {{
            border-left: 4px solid var(--accent);
            padding-left: 1.2em;
            color: #94a3b8;
            background: rgba(59, 130, 246, 0.05);
            padding: 1.2em;
            border-radius: 0 12px 12px 0;
            margin: 1.5em 0;
            font-style: italic;
        }}
        .empty-state {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: var(--text-muted);
            text-align: center;
            margin-top: 20vh;
        }}
        .empty-state svg {{ width: 80px; height: 80px; margin-bottom: 24px; opacity: 0.3; }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>AutoDocGen</h1>
            <p>全景项目分析报告</p>
        </div>
        <div class="file-list" id="fileList">
            <!-- 动态渲染 -->
        </div>
    </div>
    <div class="content-area">
        <div id="content" class="markdown-body">
            <div class="empty-state">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                <h2>请在左侧选择文件</h2>
                <p>点击左侧侧边栏的文件名，即可查看由大模型自动生成的代码解析文档。</p>
            </div>
        </div>
    </div>

    <!-- 注入的文档数据 -->
    <script id="docData" type="application/json">
        {json_data}
    </script>

    <script>
        marked.setOptions({{
            highlight: function(code, lang) {{
                const language = hljs.getLanguage(lang) ? lang : 'plaintext';
                return hljs.highlight(code, {{ language }}).value;
            }},
            langPrefix: 'hljs language-'
        }});

        const dataStr = document.getElementById('docData').textContent;
        const docs = JSON.parse(dataStr);
        const fileListEl = document.getElementById('fileList');
        const contentEl = document.getElementById('content');
        
        let activeItem = null;

        Object.keys(docs).forEach(filePath => {{
            const div = document.createElement('div');
            div.className = 'file-item';
            div.textContent = filePath;
            div.onclick = () => {{
                if (activeItem) activeItem.classList.remove('active');
                div.classList.add('active');
                activeItem = div;
                
                // 将 Markdown 渲染为 HTML
                contentEl.innerHTML = marked.parse(docs[filePath]);
            }};
            fileListEl.appendChild(div);
        }});

        // 默认选中第一个
        if(Object.keys(docs).length > 0) {{
             fileListEl.firstChild.click();
        }}
    </script>
</body>
</html>
"""


def generate_doc_for_code(file_path, code_content):
    """调用大模型分析代码并生成文档"""
    prompt = f"""
你是一个资深的研发架构师。请为以下代码文件生成一份专业的技术文档。

【文件路径】
{file_path}

【输出要求】
1. 以 `# {os.path.basename(file_path)}` 作为大标题。
2. 用一段话简述该文件的核心业务逻辑或功能。
3. 提取出其中的主要类/函数，并解释它们的输入、输出和作用。
4. 如果代码中存在潜在的优化点，可以用 `> 💡 架构师建议：` 块引用格式单独列出。
5. 全文必须使用规范的 Markdown 格式。

【源代码】
```
{code_content}
```
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, 
            messages=[
                {"role": "system", "content": "你是一个高度专业、逻辑严密的代码解析 AI 助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(Fore.RED + f"调用大模型接口失败: {str(e)}")
        return None


def select_directory():
    """弹出窗口让用户选择要解析的目录"""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_path = filedialog.askdirectory(title="请选择要生成文档的代码目录")
    return folder_path


def process_repository():
    print(Fore.CYAN + "🔎 正在等待选择目标代码仓库...")
    
    target_repo = select_directory()
    if not target_repo:
        print(Fore.RED + "❌ 操作取消: 未选择任何目录。")
        return

    print(Fore.CYAN + f"🚀 开始解析代码仓库: {target_repo}\n")
    
    # 字典用于保存所有文件的 Markdown 文档内容
    # 格式: {"相对路径": "Markdown内容"}
    all_docs = {}
        
    for root, dirs, files in os.walk(target_repo):
        # 忽略常见的隐藏文件夹和 node_modules 等
        if any(ignored in root for ignored in ['.git', '__pycache__', 'node_modules', 'venv', 'docs_output']):
            continue

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, target_repo)
                
                print(Fore.YELLOW + f"📄 读取文件: {rel_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                        
                    if not code_content.strip():
                        print(Fore.LIGHTBLACK_EX + "   空文件，已跳过。")
                        continue
                        
                    print(Fore.GREEN + f"   🤖 正在发送至大模型 ({MODEL_NAME}) 分析中...")
                    
                    doc_content = generate_doc_for_code(file_path, code_content)
                    
                    if not doc_content:
                        print(Fore.RED + f"   ⚠️ 未生成内容，跳过保存: {rel_path}\n")
                        continue
                    
                    all_docs[rel_path] = doc_content
                    print(Fore.CYAN + "   ✅ 分析完成！\n")
                    time.sleep(1) 
                    
                except Exception as e:
                    print(Fore.RED + f"   处理文件失败: {e}\n")

    # 生成最终的单个 HTML 报告文件
    if all_docs:
        print(Fore.MAGENTA + "✨ 正在生成最终的全景 HTML 分析报告...")
        # 将 Python 字典转为 JSON 字符串，转义处理以便嵌入 HTML
        json_data_str = json.dumps(all_docs, ensure_ascii=False)
        final_html = HTML_TEMPLATE.format(json_data=json_data_str)
        
        with open(OUTPUT_HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        print(Fore.GREEN + f"🎉 恭喜！全景文档已生成完毕！")
        print(Fore.GREEN + f"👉 请直接在浏览器中打开: {os.path.abspath(OUTPUT_HTML_FILE)}")
    else:
        print(Fore.YELLOW + "⚠️ 未解析到任何有效的代码文档。")


if __name__ == "__main__":
    process_repository()
