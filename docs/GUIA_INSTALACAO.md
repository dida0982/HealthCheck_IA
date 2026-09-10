# HealthCheck IA — Guia de Instalação e Execução

Este documento explica como preparar uma nova máquina para executar o projeto **HealthCheck IA**.

Repositório:

```text
https://github.com/dida0982/HealthCheck_IA
```

---

# 1. Pré-requisitos

Antes de iniciar, instale:

* Git
* Python 3
* Ollama
* VS Code, PyCharm ou outro editor de código

Confirme as instalações no terminal:

```bash
git --version
```

```bash
python --version
```

```bash
ollama --version
```

---

# 2. Clonar o projeto

Abra o CMD, PowerShell ou terminal e execute:

```bash
git clone https://github.com/dida0982/HealthCheck_IA.git
```

Entre na pasta:

```bash
cd HealthCheck_IA
```

A estrutura principal do projeto é:

```text
HealthCheck_IA/
│
├── backend/
├── data/
├── extension/
├── MVP/
└── README.md
```

---

# 3. Criar o ambiente virtual Python

Na raiz do projeto:

```bash
python -m venv .venv
```

O ambiente virtual evita conflitos entre as bibliotecas deste projeto e outros projetos instalados na máquina.

## Windows — CMD

```bash
.venv\Scripts\activate
```

## Windows — PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Depois da ativação deverá aparecer algo semelhante a:

```text
(.venv) C:\...\HealthCheck_IA>
```

---

# 4. Atualizar o pip

Execute:

```bash
python -m pip install --upgrade pip
```

---

# 5. Instalar as dependências

Execute:

```bash
pip install fastapi uvicorn requests pydantic sentence-transformers scikit-learn
```

Entre as principais bibliotecas utilizadas atualmente estão:

* FastAPI
* Uvicorn
* Requests
* Pydantic
* Sentence Transformers
* Scikit-learn

O Sentence Transformers também poderá instalar automaticamente outras dependências, como:

* PyTorch
* Transformers
* Hugging Face Hub

Por isso essa instalação pode ser maior do que as demais.

---

# 6. Preparar o Ollama

O backend atualmente utiliza o modelo:

```text
llama3.2:3b
```

Baixe o modelo:

```bash
ollama pull llama3.2:3b
```

Confirme se ele está instalado:

```bash
ollama list
```

Deverá aparecer algo semelhante a:

```text
NAME
llama3.2:3b
```

---

# 7. Testar o Ollama

Execute:

```bash
ollama run llama3.2:3b
```

Digite uma mensagem:

```text
Olá
```

Se o modelo responder, o Ollama está funcionando corretamente.

Para sair:

```text
/bye
```

O HealthCheck IA utiliza o servidor local do Ollama em:

```text
http://localhost:11434
```

---

# 8. Entrar no backend

Na raiz do projeto:

```bash
cd backend
```

A pasta contém atualmente arquivos como:

```text
backend/
│
├── main.py
├── rag.py
├── busca_semantica.py
├── carregar_documentos.py
├── teste_embedding.py
└── teste_ollama.py
```

---

# 9. Executar a API

Dentro de:

```text
HealthCheck_IA/backend
```

execute:

```bash
python -m uvicorn main:app --reload
```

Também pode funcionar:

```bash
uvicorn main:app --reload
```

A primeira inicialização pode demorar um pouco porque o projeto utiliza o modelo de embeddings:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Esse modelo poderá ser baixado automaticamente na primeira execução.

---

# 10. Confirmar se a API está funcionando

Quando aparecer:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
```

abra no navegador:

```text
http://127.0.0.1:8000
```

A resposta esperada é:

```json
{
  "mensagem": "HealthCheck IA API funcionando"
}
```

Isso confirma que o backend está ativo.

---

# 11. Abrir a documentação da API

Abra:

```text
http://127.0.0.1:8000/docs
```

O FastAPI disponibiliza automaticamente uma interface Swagger.

Nela será possível visualizar e testar os endpoints do HealthCheck IA.

Atualmente, um dos principais endpoints é:

```text
POST /analisar
```

---

# 12. Testar uma análise

No Swagger, abra:

```text
POST /analisar
```

Clique em:

```text
Try it out
```

Utilize, por exemplo:

```json
{
  "titulo": "Chá de boldo cura diabetes",
  "descricao": "O consumo de chá de boldo é capaz de curar diabetes."
}
```

Depois clique em:

```text
Execute
```

---

# 13. Fluxo atual do sistema

O funcionamento atual pode ser resumido assim:

```text
Alegação do usuário
        ↓
Backend FastAPI
        ↓
Busca semântica
        ↓
Embeddings
        ↓
Recuperação das evidências mais relevantes
        ↓
RAG
        ↓
Prompt com alegação + evidências
        ↓
Ollama
        ↓
Llama 3.2 3B
        ↓
Classificação
        ↓
Explicação
        ↓
Evidências utilizadas
```

---

# 14. Principais componentes

## main.py

É o ponto principal da API.

Responsável por:

* iniciar o FastAPI;
* receber requisições;
* chamar a busca de evidências;
* montar o RAG;
* enviar a requisição ao Ollama;
* devolver a classificação.

---

## carregar_documentos.py

Responsável por carregar os documentos da base de conhecimento e prepará-los para utilização pelo sistema.

---

## busca_semantica.py

Responsável pela recuperação das evidências mais semanticamente relacionadas à alegação analisada.

Utiliza:

```text
Sentence Transformers
```

com o modelo:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

---

## rag.py

Responsável por organizar a alegação e as evidências recuperadas em um prompt que será enviado ao LLM.

---

## Ollama

Responsável por executar localmente o modelo de linguagem.

Modelo atual:

```text
llama3.2:3b
```

---

# 15. Comandos completos para uma nova máquina

Para quem acabou de clonar o projeto:

```bash
git clone https://github.com/dida0982/HealthCheck_IA.git

cd HealthCheck_IA

python -m venv .venv

.venv\Scripts\activate

python -m pip install --upgrade pip

pip install fastapi uvicorn requests pydantic sentence-transformers scikit-learn

ollama pull llama3.2:3b

ollama list

cd backend

python -m uvicorn main:app --reload
```

Depois abrir:

```text
http://127.0.0.1:8000/docs
```

---

# 16. Trabalhando no projeto depois da instalação

Nas próximas vezes não será necessário instalar tudo novamente.

Abra o terminal dentro do projeto e execute:

```bash
cd HealthCheck_IA
```

Ative o ambiente:

```bash
.venv\Scripts\activate
```

Entre no backend:

```bash
cd backend
```

Inicie:

```bash
python -m uvicorn main:app --reload
```

---

# 17. Atualizando o projeto

Antes de começar a trabalhar, recomenda-se atualizar a branch local:

```bash
git pull origin main
```

Depois:

```bash
.venv\Scripts\activate
```

e:

```bash
cd backend
```

```bash
python -m uvicorn main:app --reload
```

---

# 18. Antes de fazer alterações

Crie uma branch própria:

```bash
git checkout -b nome-da-branch
```

Exemplo:

```bash
git checkout -b feature-validacao-rag
```

Faça as alterações e depois:

```bash
git status
```

```bash
git add .
```

```bash
git commit -m "Implementa validação do RAG"
```

```bash
git push origin feature-validacao-rag
```

Depois abra um Pull Request no GitHub.

Evite desenvolver diretamente na branch:

```text
main
```

---

# 19. Problemas comuns

## Python não encontrado

Se aparecer:

```text
'python' não é reconhecido...
```

instale o Python e confirme que a opção de adicionar o Python ao PATH está habilitada.

---

## Uvicorn não encontrado

Utilize:

```bash
python -m uvicorn main:app --reload
```

---

## Ollama não encontrado

Feche e abra novamente o terminal após instalar o Ollama.

Teste:

```bash
ollama --version
```

---

## Modelo do Ollama não encontrado

Execute:

```bash
ollama pull llama3.2:3b
```

---

## Erro de conexão com localhost:11434

Confirme que o Ollama está funcionando.

Teste:

```bash
ollama run llama3.2:3b
```

---

## Primeira inicialização lenta

Pode ser normal.

O Sentence Transformers precisa baixar o modelo de embeddings na primeira execução.

---

# 20. Checklist para novos integrantes

Antes de começar a desenvolver, confirme:

```text
[ ] Git instalado
[ ] Python instalado
[ ] Ollama instalado
[ ] Repositório clonado
[ ] Ambiente virtual criado
[ ] Ambiente virtual ativado
[ ] Dependências Python instaladas
[ ] llama3.2:3b instalado
[ ] Ollama funcionando
[ ] Backend iniciado
[ ] http://127.0.0.1:8000 funcionando
[ ] http://127.0.0.1:8000/docs funcionando
[ ] POST /analisar testado
```

Se todos os itens estiverem funcionando, o ambiente de desenvolvimento do HealthCheck IA está pronto.
