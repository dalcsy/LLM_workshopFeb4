import openai
import numpy as np
import os
import json
import dotenv
import os
from rich import print as rprint # for making fancy outputs

dotenv.load_dotenv()
# Set up OpenAI API key
openai.api_key = ''
client = openai.OpenAI(api_key='')



# Function to read abstracts from .txt files
def load_abstracts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        abstracts = [line.strip()[0:50] for line in f if line.strip()][:5]
    return abstracts

# Function to compute embeddings for a list of texts
def get_embeddings(texts, model="text-embedding-3-small"):
    embeddings = []
    for text in texts:
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        embedding = response.data[0].embedding
        embeddings.append(embedding)  # Append embeddings correctly
    return embeddings

# Function to calculate cosine similarity
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Load journal abstracts and compute embeddings
def prepare_journal_data(journal_files):
    journal_data = {}
    for journal_name, file_path in journal_files.items():
        print(f"Processing {journal_name}...")
        abstracts = load_abstracts(file_path)
        embeddings = get_embeddings(abstracts)
        journal_data[journal_name] = embeddings
    # Save embeddings for reuse
    with open("journal_embeddings.json", "w") as f:
        json.dump(journal_data, f)
    return journal_data

# Load precomputed embeddings
def load_journal_data(embeddings_file="journal_embeddings.json"):
    with open(embeddings_file, "r") as f:
        return json.load(f)

# Recommend a journal based on input abstract
def recommend_journal(abstract_embedding, journal_data):
    # Calculate similarity scores for each journal
    journal_scores = {}
    for journal_name, embeddings in journal_data.items():
        scores = [cosine_similarity(abstract_embedding, np.array(embedding)) for embedding in embeddings]
        journal_scores[journal_name] = np.max(scores)  # Use max similarity score
    # Sort journals by score
    recommended_journals = sorted(journal_scores.items(), key=lambda x: x[1], reverse=True)
    return recommended_journals

# Main script
if __name__ == "__main__":
    # Define journal files (replace with your actual file paths)
    journal_files = {
        "Nature_Genetics": "Nature_genetics_24_abstracts_only.txt",
        "Genome_Biology": "Genome_Biology_24_only.txt",
        "American_Journal_of_Human_Genetics": "American_Journal_of_Human_Genetics_24_only.txt",
        "Human_Molecular_Genetics": "Human_Molecular_Genetics_only.txt",
        "BMC_genomics": "BMC_genomics_24_only.txt"
    }

    # Check if embeddings are already computed, otherwise compute them
    if not os.path.exists("journal_embeddings.json"):
        journal_data = prepare_journal_data(journal_files)
    else:
        journal_data = load_journal_data()

    # Input new abstract
    new_abstract = "Genome-wide association studies provide a powerful means of identifying loci and genes contributing to disease, but in many cases, the related cell types/states through which genes confer disease risk remain unknown. Deciphering such relationships is important for identifying pathogenic processes and developing therapeutics. In the present study, we introduce sc-linker, a framework for integrating single-cell RNA-sequencing, epigenomic SNP-to-gene maps and genome-wide association study summary statistics to infer the underlying cell types and processes by which genetic variants influence disease. The inferred disease enrichments recapitulated known biology and highlighted notable cell–disease relationships, including γ-aminobutyric acid-ergic neurons in major depressive disorder, a disease-dependent M-cell program in ulcerative colitis and a disease-specific complement cascade process in multiple sclerosis. In autoimmune disease, both healthy and disease-dependent immune cell-type programs were associated, whereas only disease-dependent epithelial cell programs were prominent, suggesting a role in disease response rather than initiation. Our framework provides a powerful approach for identifying the cell types and cellular processes by which genetic variants influence disease."

    # Get embedding for the input abstract
    abstract_embedding = get_embeddings([new_abstract])[0]
    print("done")

    # Recommend journals
    recommendations = recommend_journal(abstract_embedding, journal_data)

    # Display recommendations
    print("\nRecommended Journals:")
    for journal, score in recommendations:
        print(f"{journal}: {score:.4f}")