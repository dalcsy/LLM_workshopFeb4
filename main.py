import openai

# OpenAI API Key（请替换为你的 API Key）
openai.api_key = "your-api-key"

# 读取期刊摘要文件
def load_abstracts(file_path):
    """加载期刊摘要文本"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 期刊摘要数据
journal_abstracts = {
    "American Journal of Human Genetics": load_abstracts("American_Journal_of_Human_Genetics_24_only.txt"),
    "BMC Genomics": load_abstracts("BMC_genomics_24_only.txt"),
    "Genome Biology": load_abstracts("Genome_Biology_24_only.txt"),
    "Human Molecular Genetics": load_abstracts("Human_Molecular_Genetics_only.txt"),
    "Nature Genetics": load_abstracts("Nature_genetics_24_abstracts_only.txt")
}

# 让用户输入摘要
your_abstract = input("\n请输入你的摘要：\n")

# 构造 OpenAI 分析 Prompt
analysis_prompt = f"""
你是一位经验丰富的学术编辑。以下是五个不同期刊的摘要数据，以及一个待投摘要。
你的任务是根据期刊摘要内容，评估该摘要最适合哪个期刊，并给出每个期刊的适合度评分（百分制）。

**待投摘要：**
{your_abstract}

**期刊摘要数据：**
{journal_abstracts}

请分析该摘要的最佳匹配期刊，并返回 JSON 格式：
{{
    "最佳期刊": "XXX",
    "匹配评分": {{
        "Nature Genetics": 85.2,
        "American Journal of Human Genetics": 78.3,
        "Genome Biology": 69.5,
        "Human Molecular Genetics": 74.1,
        "BMC Genomics": 61.8
    }}
}}
"""

# 调用 OpenAI API
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是一位资深期刊编辑，擅长评估摘要与期刊的匹配度。"},
        {"role": "user", "content": analysis_prompt}
    ]
)

# 输出 GPT-4o-mini 分析结果
gpt_analysis = response["choices"][0]["message"]["content"]
print("\n=== GPT-4o-mini 分析结果 ===\n")
print(gpt_analysis)
