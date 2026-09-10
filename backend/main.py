from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from busca_semantica import buscar_evidencias

app = FastAPI(
    title="HealthCheck IA API",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# MODELOS DE DADOS
# =========================

class AnaliseRequest(BaseModel):
    titulo: str
    descricao: str


class AnaliseResponse(BaseModel):
    classificacao: str
    confianca: float


# =========================
# ROTAS
# =========================

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

    print("Título recebido:", dados.titulo)
    print("Descrição recebida:", dados.descricao)

    # RESPOSTA SIMULADA
    return AnaliseResponse(
        classificacao="enganosa",
        confianca=0.82
    )