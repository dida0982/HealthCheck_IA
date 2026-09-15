# 🩺 HealthCheck IA — Guia de Instalação e Execução

Este documento explica como instalar e executar o **HealthCheck IA** em uma máquina Windows.

O sistema utiliza:

- Python;
- FastAPI;
- Sentence Transformers;
- Ollama;
- Qwen 2.5 7B;
- extensão para Google Chrome;
- MLflow para registro dos experimentos.

---

# 1. Pré-requisitos

Antes de iniciar, instale:

- Git;
- Python 3;
- Ollama;
- Google Chrome;
- VS Code ou outro editor de código.

Confirme as instalações:

```powershell
git --version
```

```powershell
python --version
```

```powershell
ollama --version
```

Se os três comandos retornarem suas respectivas versões, podemos continuar.

---

# 2. Clonar o repositório

Abra o PowerShell ou terminal.

Execute:

```powershell
git clone https://github.com/dida0982/HealthCheck_IA.git
```

Entre no projeto:

```powershell
cd HealthCheck_IA
```

A estrutura principal será semelhante a:

```text
HealthCheck_IA/
│
├── backend/
├── data/
├── docs/
├── extension/
├── MVP/
├── tests/
│
├── .gitignore
├── mlflow.db
├── README.md
└── requirements.txt
```

---

# 3. Criar o ambiente virtual

Na raiz do projeto:

```powershell
python -m venv backend/.venv
```

O ambiente virtual será criado em:

```text
backend/.venv/
```

Essa pasta não deve ser enviada ao GitHub.

---

# 4. Ativar o ambiente virtual

No PowerShell:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

Depois da ativação deverá aparecer algo semelhante a:

```text
(.venv) PS C:\...\HealthCheck_IA>
```

## Caso o PowerShell bloqueie a ativação

Se aparecer erro relacionado à política de execução, utilize:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois tente novamente:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

A alteração com `-Scope Process` vale somente para a sessão atual do PowerShell.

---

# 5. Atualizar o pip

Com o ambiente virtual ativo:

```powershell
python -m pip install --upgrade pip
```

---

# 6. Instalar as dependências

O projeto possui:

```text
requirements.txt
```

Portanto, não é necessário instalar cada biblioteca manualmente.

Execute na raiz do projeto:

```powershell
pip install -r requirements.txt
```

Entre as principais dependências estão:

```text
FastAPI
Uvicorn
Pydantic
Requests
Sentence Transformers
Scikit-learn
NumPy
Pandas
MLflow
```

O Sentence Transformers possui dependências adicionais e a instalação pode levar alguns minutos.

---

# 7. Preparar o Ollama

O HealthCheck IA utiliza atualmente:

```text
qwen2.5:7b
```

Baixe o modelo:

```powershell
ollama pull qwen2.5:7b
```

Depois confirme:

```powershell
ollama list
```

A lista deve conter:

```text
qwen2.5:7b
```

---

# 8. Testar o modelo

Execute:

```powershell
ollama run qwen2.5:7b
```

Digite uma mensagem simples.

Por exemplo:

```text
Olá
```

Se o modelo responder, o Ollama e o Qwen estão funcionando.

Para sair:

```text
/bye
```

---

# 9. Comunicação com o Ollama

O HealthCheck IA utiliza o servidor local disponibilizado pelo Ollama.

Normalmente ele está disponível em:

```text
http://localhost:11434
```

O backend envia as solicitações ao Ollama durante a análise das alegações.

Não é necessário manter:

```powershell
ollama run qwen2.5:7b
```

aberto interativamente durante o uso normal do projeto.

O importante é que o serviço do Ollama esteja disponível.

---

# 10. Primeira execução do backend

Com o ambiente virtual ativo, entre na pasta:

```powershell
cd backend
```

Execute:

```powershell
python -m uvicorn main:app --reload
```

Quando o backend estiver funcionando deverá aparecer uma mensagem semelhante a:

```text
Uvicorn running on http://127.0.0.1:8000
```

Mantenha esse terminal aberto enquanto utilizar o HealthCheck IA.

---

# 11. Primeira inicialização

Na primeira execução, o projeto poderá baixar o modelo de embeddings:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Por isso, a primeira inicialização pode demorar mais.

Depois do carregamento, o sistema prepara os documentos e seus chunks para a busca semântica.

A configuração atual da base possui:

```text
18 documentos
73 chunks após processamento
```

---

# 12. Swagger

Com o backend funcionando, abra:

```text
http://127.0.0.1:8000/docs
```

O FastAPI disponibiliza a interface Swagger.

O principal endpoint do HealthCheck IA é:

```text
POST /analisar
```

---

# 13. Testar o backend

No Swagger:

```text
POST /analisar
```

Clique em:

```text
Try it out
```

Exemplo:

```json
{
  "titulo": "Vacina contra gripe",
  "descricao": "A vacina contra gripe ajuda a reduzir casos graves."
}
```

Clique em:

```text
Execute
```

O sistema executará aproximadamente:

```text
Alegação
   ↓
Busca semântica
   ↓
Top 5 evidências
   ↓
RAG
   ↓
Qwen 2.5 7B
   ↓
Classificação
   ↓
Explicação
   ↓
Evidências utilizadas
```

A primeira análise também pode levar mais tempo devido ao carregamento dos modelos.

---

# 14. Carregar a extensão no Chrome

Com o backend funcionando, abra no Google Chrome:

```text
chrome://extensions/
```

Ative:

```text
Modo do desenvolvedor
```

Clique em:

```text
Carregar sem compactação
```

---

# 15. Selecionar a pasta correta

Não selecione a raiz inteira do projeto.

Errado:

```text
HealthCheck_IA/
```

Correto:

```text
HealthCheck_IA/extension/
```

O Chrome precisa encontrar diretamente:

```text
manifest.json
```

A pasta selecionada deve conter:

```text
extension/
├── manifest.json
├── content.js
├── styles.css
└── teste-visual.html
```

Selecione:

```text
extension
```

A extensão deverá aparecer na página de extensões do Chrome.

Mantenha-a ativada.

---

# 16. Atualizar a extensão após alterações

Se modificar:

```text
content.js
manifest.json
styles.css
```

abra:

```text
chrome://extensions/
```

e clique no botão de atualização da extensão.

Depois recarregue a página do Google utilizada no teste.

---

# 17. Executar o sistema completo

Com o backend e o Ollama disponíveis e a extensão carregada:

```text
Usuário
   ↓
Pesquisa no Google
   ↓
Chrome Extension
   ↓
Captura do resultado
   ↓
FastAPI
   ↓
Busca semântica
   ↓
Top 5 evidências
   ↓
RAG
   ↓
Ollama
   ↓
Qwen 2.5 7B
   ↓
Classificação + explicação
   ↓
FastAPI
   ↓
Chrome Extension
   ↓
Card HealthCheck IA
```

---

# 18. Teste no Google

Realize uma pesquisa relacionada a um dos temas da base.

Exemplos:

```text
vacina contra gripe
dengue
diabetes
hipertensão
câncer
medicamentos
```

A extensão detectará resultados compatíveis com seu mecanismo atual e enviará as análises ao backend.

Como cada resultado analisado pode gerar uma chamada ao modelo local, várias análises simultâneas podem utilizar bastante CPU, memória e outros recursos da máquina.

Para testes técnicos do modelo, prefira o Swagger quando não for necessário validar a integração com o Google.

---

# 19. Teste visual sem executar IA

Existe:

```text
extension/teste-visual.html
```

Esse arquivo permite verificar visualmente os cinco estados da interface sem executar:

```text
FastAPI
Ollama
Qwen
embeddings
busca no Google
```

Os cinco estados são:

```text
🟢 Evidências favoráveis
🟡 Evidências parcialmente favoráveis
🟠 Informação potencialmente enganosa
🔴 Evidências contraditórias
⚪ Evidências insuficientes
```

Esse recurso é recomendado quando o objetivo é testar apenas a interface.

---

# 20. Execução diária

Depois da primeira instalação, não é necessário reinstalar as dependências ou baixar novamente o modelo.

Abra o PowerShell na raiz do projeto.

Ative o ambiente:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

Entre no backend:

```powershell
cd backend
```

Execute:

```powershell
python -m uvicorn main:app --reload
```

Depois utilize:

```text
http://127.0.0.1:8000/docs
```

ou a extensão no Google Chrome.

---

# 21. Encerrar o backend

No terminal onde o Uvicorn está executando, pressione:

```text
Ctrl + C
```

Isso encerra o servidor FastAPI.

---

# 22. Desativar o ambiente virtual

Execute:

```powershell
deactivate
```

---

# 23. MLflow

O HealthCheck IA utiliza MLflow para registrar os experimentos da avaliação científica.

O armazenamento oficial atual é:

```text
mlflow.db
```

O experimento final é:

```text
HealthCheck_IA_Avaliacao_Final
```

Run:

```text
qwen2.5_7b_avaliacao_final_200
```

---

# 24. Abrir o MLflow

Na raiz do projeto, com o ambiente virtual disponível, execute:

```powershell
.\backend\.venv\Scripts\python.exe -m mlflow ui --backend-store-uri "sqlite:///mlflow.db" --port 5001
```

Abra:

```text
http://127.0.0.1:5001
```

O experimento do HealthCheck IA poderá ser consultado pela interface do MLflow.

Para encerrar:

```text
Ctrl + C
```

---

# 25. Atualizar o projeto pelo Git

Antes de trabalhar em uma cópia já existente:

```powershell
git pull origin main
```

Verifique:

```powershell
git status
```

---

# 26. Problemas comuns

## Python não encontrado

Se:

```text
python
```

não for reconhecido, verifique a instalação do Python e sua configuração no PATH.

---

## Ollama não encontrado

Teste:

```powershell
ollama --version
```

Se necessário, feche e abra novamente o terminal após instalar o Ollama.

---

## Modelo não encontrado

Execute:

```powershell
ollama pull qwen2.5:7b
```

Confirme:

```powershell
ollama list
```

---

## Backend não inicia

Confirme que o ambiente virtual está ativo:

```text
(.venv)
```

Depois verifique as dependências:

```powershell
pip install -r requirements.txt
```

---

## Erro ao carregar a extensão

Confirme que foi selecionada:

```text
HealthCheck_IA/extension/
```

e não:

```text
HealthCheck_IA/
```

O arquivo:

```text
manifest.json
```

deve estar diretamente dentro da pasta selecionada.

---

## Extensão não consegue analisar

Verifique se o backend está funcionando:

```text
http://127.0.0.1:8000/docs
```

Também confirme que o Ollama está disponível e que:

```text
qwen2.5:7b
```

está instalado.

---

## Primeira execução lenta

Pode ser normal.

O modelo de embeddings pode precisar ser baixado e carregado na primeira execução.

O Qwen também utiliza recursos consideráveis da máquina durante as análises.

---

# 27. Checklist de instalação

Antes de utilizar o sistema completo:

```text
[ ] Git instalado
[ ] Python instalado
[ ] Ollama instalado
[ ] Google Chrome instalado
[ ] Repositório clonado
[ ] backend/.venv criado
[ ] Ambiente virtual ativado
[ ] requirements.txt instalado
[ ] qwen2.5:7b instalado
[ ] Ollama disponível
[ ] Backend funcionando
[ ] Swagger funcionando
[ ] POST /analisar testado
[ ] Extensão carregada
[ ] Pasta extension selecionada corretamente
```

---

# 28. Sequência rápida — primeira instalação

```powershell
git clone https://github.com/dida0982/HealthCheck_IA.git

cd HealthCheck_IA

python -m venv backend/.venv

.\backend\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

ollama pull qwen2.5:7b

ollama list

cd backend

python -m uvicorn main:app --reload
```

Depois:

```text
http://127.0.0.1:8000/docs
```

E no Chrome:

```text
chrome://extensions/
→ Modo do desenvolvedor
→ Carregar sem compactação
→ selecionar HealthCheck_IA/extension/
```

---

# 29. Sequência rápida — uso diário

Na raiz do projeto:

```powershell
.\backend\.venv\Scripts\Activate.ps1

cd backend

python -m uvicorn main:app --reload
```

Depois utilize o Swagger ou a extensão.

---

## HealthCheck IA

**Inteligência Artificial + Evidências + Pensamento Crítico**

Se o backend, o Ollama e a extensão estiverem funcionando, o ambiente está pronto para executar o HealthCheck IA.