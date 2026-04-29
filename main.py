import os
import time
from pathlib import Path
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

# 初始化客户端 (支持所有兼容 OpenAI 格式的 API，如 OpenAI, Gemini, DeepSeek, MIMO 等)
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# ========================
# 配置区
# ========================
TARGET_REPO = "test_repo" 
OUTPUT_DIR = "docs_output"

SUPPORTED_EXTENSIONS = ['.py', '.js', '.java', '.cpp', '.c', '.go', '.ts', '.html', '.css']


def generate_doc_for_code(file_path, code_content):
    """调用大模型分析代码并生成文档"""
    prompt = f"""
你是一个资深的研发架构师。请为以下代码文件生成一份专业的技术文档。

【文件路径】
{file_path}

【输出要求】
1. 用一两句话简述该文件的核心业务逻辑或功能。
2. 提取出其中的主要类/函数，并解释它们的输入、输出和作用。
3. 如果代码中存在潜在的优化点，可以用“💡 架构师建议”单独列出。
4. 全文必须使用规范的 Markdown 格式，排版清晰美观。

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
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(Fore.RED + f"调用大模型接口失败: {str(e)}")
        print(Fore.YELLOW + "👉 提示: 请检查 .env 中的 BASE_URL 和 MODEL_NAME 是否与你使用的模型相匹配。")
        return None


def process_repository():
    print(Fore.CYAN + f"🚀 开始解析代码仓库: {TARGET_REPO}")
    print(Fore.CYAN + f"📂 输出目录: {OUTPUT_DIR}\n")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    if not os.path.exists(TARGET_REPO):
        print(Fore.RED + f"❌ 找不到目标目录 '{TARGET_REPO}'，请检查配置。")
        return

    for root, dirs, files in os.walk(TARGET_REPO):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                print(Fore.YELLOW + f"📄 正在读取文件: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                        
                    if not code_content.strip():
                        print(Fore.LIGHTBLACK_EX + "   空文件，已跳过。")
                        continue
                        
                    print(Fore.GREEN + f"   🤖 正在发送至大模型 ({MODEL_NAME}) 分析中...")
                    
                    doc_content = generate_doc_for_code(file_path, code_content)
                    
                    if not doc_content:
                        print(Fore.RED + f"   ⚠️ 未生成内容，跳过保存: {file_path}\n")
                        continue
                    
                    rel_path = os.path.relpath(file_path, TARGET_REPO)
                    doc_file_name = rel_path.replace(os.sep, '_') + '.md'
                    out_path = os.path.join(OUTPUT_DIR, doc_file_name)
                    
                    with open(out_path, 'w', encoding='utf-8') as out_f:
                        out_f.write(doc_content)
                        
                    print(Fore.CYAN + f"   ✅ 解析完成，文档已保存至: {out_path}\n")
                    
                    time.sleep(1) 
                    
                except Exception as e:
                    print(Fore.RED + f"   处理文件失败: {e}\n")


if __name__ == "__main__":
    process_repository()
    print(Fore.GREEN + "🎉 所有代码文档生成完毕！")
