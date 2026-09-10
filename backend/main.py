from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from busca_semantica import buscar_evidencias


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

    evidencias = buscar_evidencias(
        texto_para_analisar,
        top_k=3
    )

    return AnaliseResponse(
        evidencias=evidencias
    )