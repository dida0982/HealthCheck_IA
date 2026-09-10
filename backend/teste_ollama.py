import json
import requests

from rag import montar_prompt_rag


alegacao = "A vacina contra gripe ajuda a evitar casos graves?"

prompt = montar_prompt_rag(
    alegacao,
    top_k=3
)

url = "http://localhost:11434/api/generate"

dados = {
    "model": "llama3.2:3b",
    "prompt": prompt,
    "stream": False
}

resposta = requests.post(
    url,
    json=dados
)

resultado = resposta.json()

resposta_llm = resultado["response"]

analise = json.loads(resposta_llm)

print("\n=== ANÁLISE DO HEALTHCHECK IA ===\n")

print("Classificação:")
print(analise["classificacao"])

print("\nExplicação:")
print(analise["explicacao"])

print("\nEvidências utilizadas:")
print(analise["evidencias_utilizadas"])