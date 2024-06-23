from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API key:" + api_key[0:6])
else:
    print("API key not found.")

documents = SimpleDirectoryReader("pdf").load_data()



#%%

index = VectorStoreIndex.from_documents(documents)

engine = index.as_query_engine()

result = engine.query("What are the strengths of R over python?")
print(result)

#%%

index.storage_context.persist("ml_index")
print("Done")
# %%
