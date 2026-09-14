import requests


url = "http://localhost:11434/api/generate"

prompt = """
Analise somente se existe contradição entre a ALEGAÇÃO e a EVIDÊNCIA.

ALEGAÇÃO:
A principal forma de transmissão da dengue ocorre pelo contato direto
entre uma pessoa infectada e outra pessoa.

EVIDÊNCIA:
A principal forma de transmissão da dengue ocorre pela picada da fêmea
do mosquito Aedes aegypti infectada pelo vírus.

Existe contradição entre as duas afirmações?

Responda SOMENTE:

SIM

ou

NÃO
"""


dados = {
    "model": "qwen2.5:7b",
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0
    }
}


resposta = requests.post(
    url,
    json=dados,
    timeout=300
)

resposta.raise_for_status()

resultado = resposta.json()

print("Resposta do modelo:")
print(resultado["response"])