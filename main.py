import openai

# OpenAI API Key (replace with your actual API key)
openai.api_key = "your-api-key"

# Function to read abstract files
def load_abstracts(file_path):
    """Loads abstracts from a given text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Load abstracts from journal files
journal_abstracts = {
    "American Journal of Human Genetics": load_abstracts("American_Journal_of_Human_Genetics_24_only.txt"),
    "BMC Genomics": load_abstracts("BMC_genomics_24_only.txt"),
    "Genome Biology": load_abstracts("Genome_Biology_24_only.txt"),
    "Human Molecular Genetics": load_abstracts("Human_Molecular_Genetics_only.txt"),
    "Nature Genetics": load_abstracts("Nature_genetics_24_abstracts_only.txt")
}

# Ask the user to input their abstract
your_abstract = input("\nEnter your abstract:\n")

# Construct the prompt for GPT-4o-mini
analysis_prompt = f"""
You are an experienced academic journal editor. Below are abstracts from five different journals, along with a research abstract.
Your task is to evaluate which journal is the best fit for the given abstract and provide suitability scores (in percentage) for each journal.

**Research Abstract to Evaluate:**
{your_abstract}

**Journal Abstract Data:**
{journal_abstracts}

Please analyze this abstract and return a JSON-formatted response:
{{
    "Best Journal": "XXX",
    "Suitability Scores": {{
        "Nature Genetics": 85.2,
        "American Journal of Human Genetics": 78.3,
        "Genome Biology": 69.5,
        "Human Molecular Genetics": 74.1,
        "BMC Genomics": 61.8
    }}
}}
"""

# Call OpenAI API for analysis
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a seasoned journal editor specializing in evaluating abstracts for academic publications."},
        {"role": "user", "content": analysis_prompt}
    ]
)

# Extract GPT-4o-mini's response
gpt_analysis = response["choices"][0]["message"]["content"]
print("\n=== GPT-4o-mini Analysis Result ===\n")
print(gpt_analysis)