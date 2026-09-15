# 💻 HealthCheck IA — Comandos de Terminal

Este arquivo é uma referência rápida dos principais comandos utilizados no **HealthCheck IA**.

Para explicações detalhadas sobre instalação e configuração, consulte:

```text
docs/GUIA_INSTALACAO.md
```

---

# 1. Clonar o projeto

```powershell
git clone https://github.com/dida0982/HealthCheck_IA.git
```

```powershell
cd HealthCheck_IA
```

---

# 2. Criar o ambiente virtual

Na raiz do projeto:

```powershell
python -m venv backend/.venv
```

---

# 3. Ativar o ambiente virtual

PowerShell:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execução:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

---

# 4. Atualizar o pip

```powershell
python -m pip install --upgrade pip
```

---

# 5. Instalar as dependências

Na raiz do projeto:

```powershell
pip install -r requirements.txt
```

---

# 6. Verificar dependências instaladas

```powershell
pip list
```

Ou:

```powershell
pip freeze
```

---

# 7. Ollama

Verificar instalação:

```powershell
ollama --version
```

Baixar o modelo utilizado pelo HealthCheck IA:

```powershell
ollama pull qwen2.5:7b
```

Listar modelos:

```powershell
ollama list
```

Testar o modelo:

```powershell
ollama run qwen2.5:7b
```

Sair do modo interativo:

```text
/bye
```

---

# 8. Executar o backend

Na raiz do projeto, ative o ambiente:

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

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 9. Encerrar o backend

No terminal do Uvicorn:

```text
Ctrl + C
```

---

# 10. Desativar o ambiente virtual

```powershell
deactivate
```

---

# 11. Extensão Chrome

Abra no Chrome:

```text
chrome://extensions/
```

Depois:

```text
Modo do desenvolvedor
        ↓
Carregar sem compactação
        ↓
HealthCheck_IA/extension/
```

A pasta selecionada deve conter diretamente:

```text
manifest.json
content.js
styles.css
teste-visual.html
```

---

# 12. Teste visual

Arquivo:

```text
extension/teste-visual.html
```

Utilize esse arquivo quando quiser verificar apenas a interface das cinco classificações sem executar o modelo de IA.

---

# 13. MLflow

Na raiz do projeto:

```powershell
.\backend\.venv\Scripts\python.exe -m mlflow ui --backend-store-uri "sqlite:///mlflow.db" --port 5001
```

Abra:

```text
http://127.0.0.1:5001
```

Experimento:

```text
HealthCheck_IA_Avaliacao_Final
```

Run:

```text
qwen2.5_7b_avaliacao_final_200
```

Para encerrar o MLflow:

```text
Ctrl + C
```

---

# 14. Git — verificar situação

```powershell
git status
```

---

# 15. Git — atualizar projeto local

```powershell
git pull origin main
```

---

# 16. Git — verificar branch atual

```powershell
git branch
```

---

# 17. Git — criar uma nova branch

```powershell
git checkout -b nome-da-branch
```

Exemplo:

```powershell
git checkout -b feature-nova-funcionalidade
```

---

# 18. Git — adicionar alterações

Arquivo específico:

```powershell
git add caminho/do/arquivo
```

Todos os arquivos modificados:

```powershell
git add .
```

Antes de usar `git add .`, confira:

```powershell
git status
```

---

# 19. Git — criar commit

```powershell
git commit -m "Descricao da alteracao"
```

---

# 20. Git — enviar para o GitHub

Branch principal:

```powershell
git push origin main
```

Outra branch:

```powershell
git push origin nome-da-branch
```

---

# 21. Git — histórico recente

```powershell
git log --oneline -10
```

---

# 22. Verificar arquivos rastreados indesejados

Verificar cache Python:

```powershell
git ls-files | Select-String "__pycache__"
```

Verificar `mlruns/`:

```powershell
git ls-files | Select-String "^mlruns/"
```

Se os comandos não retornarem resultados, esses arquivos não estão sendo rastreados pelo Git.

---

# 23. Executar avaliação final

Com o ambiente virtual configurado:

```powershell
.\backend\.venv\Scripts\python.exe .\tests\executar_avaliacao_final.py
```

Esse processo executa múltiplas análises com o modelo local e pode utilizar bastante recurso computacional.

Não execute novamente apenas para consultar métricas já registradas.

---

# 24. Calcular métricas

```powershell
.\backend\.venv\Scripts\python.exe .\tests\calcular_metricas.py
```

Resultados da avaliação oficial atual:

```text
Alegações: 200
Acertos: 151
Erros: 49

Accuracy: 75,50%
Precision macro: 79,72%
Recall macro: 75,50%
F1-score macro: 72,87%
```

---

# 25. Registrar experimento no MLflow

```powershell
.\backend\.venv\Scripts\python.exe .\tests\registrar_mlflow.py
```

O experimento oficial já está registrado em:

```text
mlflow.db
```

Não é necessário executar novamente apenas para visualizar o resultado.

---

# 26. Sequência — primeira instalação

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
Swagger:
http://127.0.0.1:8000/docs

Chrome:
chrome://extensions/
```

No Chrome:

```text
Modo do desenvolvedor
        ↓
Carregar sem compactação
        ↓
selecionar HealthCheck_IA/extension/
```

---

# 27. Sequência — uso diário

Partindo da raiz:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

```powershell
cd backend
```

```powershell
python -m uvicorn main:app --reload
```

Depois utilize:

```text
http://127.0.0.1:8000/docs
```

ou a extensão do HealthCheck IA no Chrome.

---

# 28. Sequência — encerrar ambiente

Parar o backend:

```text
Ctrl + C
```

Desativar o ambiente:

```powershell
deactivate
```

---

# 29. Sequência — enviar uma alteração para a main

Primeiro:

```powershell
git status
```

Depois:

```powershell
git add caminho/do/arquivo
```

```powershell
git commit -m "Descricao da alteracao"
```

```powershell
git push origin main
```

Confirme:

```powershell
git status
```

---

# 30. Resumo dos serviços locais

```text
FastAPI
http://127.0.0.1:8000

Swagger
http://127.0.0.1:8000/docs

Ollama
http://localhost:11434

MLflow
http://127.0.0.1:5001
```

---

## HealthCheck IA

**Inteligência Artificial + Evidências + Pensamento Crítico**