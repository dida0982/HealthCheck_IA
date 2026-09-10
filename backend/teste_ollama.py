import json
import requests

from busca_semantica import buscar_evidencias
from rag import montar_prompt_rag


alegacao = "A vacina contra gripe ajuda a evitar casos graves?"


# 1. Busca as evidências uma única vez
evidencias = buscar_evidencias(
    alegacao,
    top_k=3
)


# 2. Monta o prompt usando as evidências encontradas
prompt = montar_prompt_rag(
    alegacao,
    evidencias
)


# 3. Configura a comunicação com o Ollama
url = "http://localhost:11434/api/generate"

dados = {
    "model": "llama3.2:3b",
    "prompt": prompt,
    "stream": False
}


# 4. Envia o prompt para o Ollama
resposta = requests.post(
    url,
    json=dados
)

resultado = resposta.json()


# 5. Obtém a resposta do LLM
resposta_llm = resultado["response"]


# 6. Converte o JSON retornado pelo LLM em objeto Python
analise = json.loads(resposta_llm)


# 7. Exibe os campos separadamente
print("\n=== ANÁLISE DO HEALTHCHECK IA ===\n")

print("Classificação:")
print(analise["classificacao"])

print("\nExplicação:")
print(analise["explicacao"])

print("\nEvidências utilizadas:")
print(analise["evidencias_utilizadas"])