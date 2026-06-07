from src.retriever import Retriever
from src.prompt_builder import PromptBuilder

r = Retriever()
p = PromptBuilder()

docs = r.search("What is AWS Lambda?")
prompt = p.build("What is AWS Lambda?", docs)

print(prompt)