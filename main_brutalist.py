import os
import dotenv
from openai import OpenAI
from rich import print as rprint  # Fancy output formatting

# 加载 .env 文件（API Key 自动读取）
dotenv.load_dotenv()

# 初始化 OpenAI 客户端
client = OpenAI()

# 读取摘要文件的函数（只取前 5 行，每行最多 50 个字符）
def load_abstracts(file_path, num_lines=5, char_limit=50):
    """从文本文件中读取前 num_lines 行，并限制每行最多 char_limit 个字符"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # 只取前 num_lines 行，每行最多取 char_limit 个字符
            processed_abstracts = [line[:char_limit] for line in lines[:num_lines]]
            return "\n".join(processed_abstracts)  # 以换行符拼接成字符串
    except FileNotFoundError:
        rprint(f"[bold red]Error:[/bold red] File '{file_path}' not found!")
        return None

# 期刊摘要文件
journal_files = {
    "American Journal of Human Genetics": "American_Journal_of_Human_Genetics_24_only.txt",
    "BMC Genomics": "BMC_genomics_24_only.txt",
    "Genome Biology": "Genome_Biology_24_only.txt",
    "Human Molecular Genetics": "Human_Molecular_Genetics_only.txt",
    "Nature Genetics": "Nature_genetics_24_abstracts_only.txt"
}

journal_abstracts = {}

# 读取每个期刊摘要的前 5 行，每行最多 50 个字符
rprint("\n[bold blue]=== Journal Abstracts Preview (Limited) ===[/bold blue]\n")
for journal, file_path in journal_files.items():
    abstracts = load_abstracts(file_path)
    if abstracts:
        journal_abstracts[journal] = abstracts
        rprint(f"\n[bold yellow]--- {journal} ---[/bold yellow]\n")
        rprint(abstracts)  # 打印处理后的摘要
        rprint("\n----------------------------\n")

# 确保所有文件都成功加载
if not all(journal_abstracts.values()):
    rprint("\n[bold red]Error:[/bold red] Some journal abstract files were not loaded properly. Check the file paths and try again.")
    exit()

# 让用户输入自己的摘要
your_abstract = input("\n[bold green]Enter your abstract:[/bold green]\n")

# 构造 GPT-4o-mini 的 Prompt
analysis_prompt = f"""
You are an experienced academic journal editor. Below are shortened abstracts from five different journals, along with a research abstract.
Your task is to evaluate which journal is the best fit for the given abstract and provide suitability scores (in percentage) for each journal.

**Research Abstract to Evaluate:**
{your_abstract}

**Shortened Journal Abstracts (First 5 entries, first 50 chars each):**
{journal_abstracts}

Please analyze this abstract and return a JSON-formatted response:
{{
    "Best Journal": "XXX",
    "Suitability Scores": {{
        "Nature Genetics": xxx,
        "American Journal of Human Genetics": xxx,
        "Genome Biology": xxx,
        "Human Molecular Genetics": xxx,
        "BMC Genomics": xxx
    }}
}}
"""

# 调用 OpenAI API 进行摘要匹配
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a seasoned journal editor specializing in evaluating abstracts for academic publications."},
        {"role": "user", "content": analysis_prompt}
    ],
    max_tokens=256
)

# 提取 OpenAI 的分析结果
gpt_analysis = response.choices[0].message.content

# 打印最终分析结果
rprint("\n[bold blue]=== GPT-4o-mini Analysis Result ===[/bold blue]\n")
rprint(gpt_analysis)
