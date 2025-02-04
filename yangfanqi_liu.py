
##Retrieve the OpenAI api
from openai import OpenAI
import dotenv
import os
from rich import print as rprint # for making fancy outputs

dotenv.load_dotenv()

client = OpenAI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



##Calling ChatGPT
system_prompt = "You are Matsuo Basho, the great Japanese haiku poet."
user_query = "Can you give me a haiku about a Samurai cat."

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_query},
  ],
  max_tokens=128,
  stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")