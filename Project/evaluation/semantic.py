import json
import subprocess
import requests
import os 
import sys
import urllib.parse
from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    final_str = f"{{!knn f=vector topK=20}}{embedding_str}"
    print(final_str)
    return final_str

def getParameters(query: int, mode: str) -> json:
    path = "./q6/parameters.json"
    with open(path, 'r') as file:
        data = json.load(file)
        data["semantic"]["q"] = text_to_embedding(data["semantic"]["q"])
        file.close()

    return data.get('semantic', {})

def getRequest(parameters: json) -> str:
    query_string = urllib.parse.urlencode(parameters, quote_via=urllib.parse.quote)
    return 'http://localhost:8983/solr/hotels/select?' + query_string


path = f"./q6/result-semantic.json"
parameters = getParameters(6, 'semantic')

request = getRequest(parameters)


headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

print(parameters)
result = requests.post("http://localhost:8983/solr/hotels/select", data=parameters, headers=headers).json()

print(result)
docs = result.get("response", {}).get("docs", [])

with open(path, 'w') as file:
    file.write(json.dumps(docs, indent=2))
    file.close()


