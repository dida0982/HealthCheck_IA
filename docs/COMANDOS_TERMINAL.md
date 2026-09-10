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

Claro. Você pode acrescentar esta seção no `COMANDOS_TERMINAL.md`:

````markdown
# Carregar a extensão no Google Chrome

Depois de iniciar o backend, é necessário carregar a extensão do projeto manualmente no Chrome.

## 1. Abrir a página de extensões

No Google Chrome, digite na barra de endereço:

```text
chrome://extensions/
````

Pressione Enter.

---

## 2. Ativar o modo de desenvolvedor

No canto superior direito da página, ative:

```text
Modo do desenvolvedor
```

Quando ele estiver ativado, aparecerão alguns botões no topo da página, incluindo:

```text
Carregar sem compactação
Compactar extensão
Atualizar
```

Para executar o HealthCheck IA durante o desenvolvimento, utilize:

```text
Carregar sem compactação
```

Não utilize:

```text
Compactar extensão
```

A opção "Compactar extensão" serve para criar um pacote da extensão para distribuição. Ela não é necessária para executar o projeto localmente.

---

## 3. Selecionar a pasta correta

Clique em:

```text
Carregar sem compactação
```

Depois navegue até a pasta onde o projeto foi clonado.

Exemplo:

```text
C:\Users\SEU_USUARIO\OneDrive\Área de Trabalho\HealthCheck_IA
```

IMPORTANTE:

Não selecione a pasta principal:

```text
HealthCheck_IA
```

Isso causará um erro semelhante a:

```text
Falha ao carregar extensão

O arquivo de manifesto está faltando ou não pode ser lido.
Não foi possível carregar o manifesto.
```

Isso acontece porque o Chrome procura o arquivo:

```text
manifest.json
```

diretamente dentro da pasta selecionada.

No HealthCheck IA, o arquivo `manifest.json` está dentro da pasta:

```text
HealthCheck_IA\extension
```

Portanto, entre na pasta:

```text
extension
```

e selecione essa pasta.

O caminho correto deverá ser semelhante a:

```text
C:\Users\SEU_USUARIO\OneDrive\Área de Trabalho\HealthCheck_IA\extension
```

---

## 4. Estrutura esperada da extensão

Dentro da pasta selecionada devem existir arquivos semelhantes a:

```text
extension/
│
├── manifest.json
├── content.js
└── styles.css
```

O arquivo mais importante para o carregamento pelo Chrome é:

```text
manifest.json
```

Se o Chrome não encontrar esse arquivo diretamente dentro da pasta selecionada, a extensão não será carregada.

---

## 5. Confirmar o carregamento

Depois de selecionar:

```text
HealthCheck_IA\extension
```

a extensão deverá aparecer na página:

```text
chrome://extensions/
```

com o nome:

```text
HealthCheck IA
```

Deixe a extensão ativada.

---

# Resumo rápido

ERRADO:

```text
Carregar sem compactação
        ↓
HealthCheck_IA
```

CORRETO:

```text
Carregar sem compactação
        ↓
HealthCheck_IA
        ↓
extension
        ↓
Selecionar pasta
```

Caminho final:

```text
...\HealthCheck_IA\extension
```

O Chrome encontrará:

```text
extension\manifest.json
```

e conseguirá carregar a extensão corretamente.

```

Essa explicação fica boa logo **depois da parte em que você inicia o FastAPI e abre `http://127.0.0.1:8000/docs`**, porque o fluxo natural do colega será: **backend funcionando → carregar extensão no Chrome → testar o sistema**.
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
