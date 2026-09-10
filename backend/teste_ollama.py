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

print("\n=== RESPOSTA DO HEALTHCHECK IA ===\n")
print(resultado["response"])