# LLM_workshopFeb4

In this project, we hope to create a journal recommendation tool while you have a manuscript ready.

For this, we will select five representative journals in your research field at different impact levels, refer to abstracts from papers published in 2024, and figure out the similarity between our own abstract and abstracts from these already published papers.

We have two plans:

A. Feed reference abstracts in journals directly to GPT-4o mini and ask it to compare these with our abstract provided

B. Generate embeddings from [text-embedding-3-small](https://openai.com/index/new-embedding-models-and-api-updates/) and feed embeddings generated of the reference abstracts vs embeddings of our abstract provided into GPT-4o mini

and we'll compare the results generated from both plans.
