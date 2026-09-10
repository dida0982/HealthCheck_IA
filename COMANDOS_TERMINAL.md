# HealthCheck IA — Comandos de Terminal

Este arquivo reúne apenas os comandos necessários para preparar e executar o projeto em uma máquina Windows.

## Primeira instalação

### 1. Clonar o repositório

```bat
git clone https://github.com/dida0982/HealthCheck_IA.git
```

### 2. Entrar no projeto

```bat
cd HealthCheck_IA
```

### 3. Criar o ambiente virtual

```bat
python -m venv .venv
```

### 4. Ativar o ambiente virtual

CMD:

```bat
.venv\Scripts\activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Atualizar o pip

```bat
python -m pip install --upgrade pip
```

### 6. Instalar as dependências

```bat
pip install fastapi uvicorn requests pydantic sentence-transformers scikit-learn
```

### 7. Baixar o modelo do Ollama

```bat
ollama pull llama3.2:3b
```

### 8. Confirmar o modelo instalado

```bat
ollama list
```

### 9. Testar o Ollama

```bat
ollama run llama3.2:3b
```

Para sair do modelo:

```text
/bye
```

### 10. Entrar no backend

```bat
cd backend
```

### 11. Rodar a API

```bat
python -m uvicorn main:app --reload
```

### 12. Abrir a documentação da API

No navegador:

```text
http://127.0.0.1:8000/docs
```

---

# Execução diária

Depois que o ambiente já estiver configurado, nas próximas vezes basta:

```bat
cd HealthCheck_IA
```

```bat
.venv\Scripts\activate
```

```bat
cd backend
```

```bat
python -m uvicorn main:app --reload
```

Depois abrir:

```text
http://127.0.0.1:8000/docs
```

---

# Atualizar o projeto antes de trabalhar

Na raiz do projeto:

```bat
git pull origin main
```

Depois:

```bat
.venv\Scripts\activate
```

```bat
cd backend
```

```bat
python -m uvicorn main:app --reload
```

---

# Criar uma branch para trabalhar

```bat
git checkout -b nome-da-branch
```

Exemplo:

```bat
git checkout -b feature-validacao-rag
```

---

# Enviar alterações para o GitHub

```bat
git status
```

```bat
git add .
```

```bat
git commit -m "Descrição da alteração"
```

```bat
git push origin nome-da-branch
```

---

# Sequência completa — primeira vez

```bat
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

Abrir:

```text
http://127.0.0.1:8000/docs
```
