import json
import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from busca_semantica import buscar_evidencias
from rag import montar_prompt_rag


app = FastAPI(
    title="HealthCheck IA API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnaliseRequest(BaseModel):
    titulo: str
    descricao: str


class Evidencia(BaseModel):
    arquivo: str
    chunk_id: int
    conteudo: str
    similaridade: float


class AnaliseResponse(BaseModel):
    classificacao: str
    explicacao: str
    evidencias_utilizadas: list[int]
    evidencias: list[Evidencia]


@app.get("/")
def raiz():
    return {
        "mensagem": "HealthCheck IA API funcionando"
    }


@app.post(
    "/analisar",
    response_model=AnaliseResponse
)
def analisar(dados: AnaliseRequest):

    texto_para_analisar = (
        dados.titulo
        + " "
        + dados.descricao
    )

    # 1. Busca as evidências
    evidencias = buscar_evidencias(
        texto_para_analisar,
        top_k=3
    )

    # 2. Monta o prompt RAG com as mesmas evidências
    prompt = montar_prompt_rag(
        texto_para_analisar,
        evidencias
    )

    # 3. Envia o prompt para o Ollama
    url_ollama = "http://localhost:11434/api/generate"

    dados_ollama = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }

    try:

        resposta_ollama = requests.post(
            url_ollama,
            json=dados_ollama,
            timeout=300
        )

        resposta_ollama.raise_for_status()

    except requests.RequestException as erro:

        raise HTTPException(
            status_code=503,
            detail=f"Erro ao conectar com o Ollama: {erro}"
        )

    # 4. Obtém a resposta do modelo
    resultado_ollama = resposta_ollama.json()

    resposta_llm = resultado_ollama["response"]

    # 5. Converte o JSON retornado pelo LLM
    try:

        analise = json.loads(resposta_llm)

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="O LLM retornou uma resposta que não é um JSON válido."
        )

    # 6. Retorna tudo para quem chamou a API
    return AnaliseResponse(
        classificacao=analise["classificacao"],
        explicacao=analise["explicacao"],
        evidencias_utilizadas=analise["evidencias_utilizadas"],
        evidencias=evidencias
    )