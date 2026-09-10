from pathlib import Path

pasta_data = Path("../data")

documentos = []
arquivos_vazios = []
documentos_invalidos = []

def dividir_em_chunks(texto, tamanho_maximo=500):
    paragrafos = texto.split("\n\n")

    chunks = []
    chunk_atual = ""

    for paragrafo in paragrafos:
        paragrafo = paragrafo.strip()

        if not paragrafo:
            continue

        if len(chunk_atual) + len(paragrafo) <= tamanho_maximo:
            chunk_atual += paragrafo + "\n\n"

        else:
            if chunk_atual:
                chunks.append(chunk_atual.strip())

            chunk_atual = paragrafo + "\n\n"

    if chunk_atual:
        chunks.append(chunk_atual.strip())

    return chunks

for arquivo in pasta_data.rglob("*.md"):
    
    chunks = [] 
    
    for documento in documentos: 
        partes = dividir_em_chunks(documento["conteudo"]) 
        
        for indice, parte in enumerate(partes): 
            chunks.append({ 
                "arquivo": documento["arquivo"], 
                "chunk_id": indice, 
                "conteudo": parte })
    
    conteudo = arquivo.read_text(encoding="utf-8")

    if conteudo.strip():

        campos_obrigatorios = [
            "Fonte:",
            "URL:",
            "Tema:",
            "## Resumo",
            "## Evidências importantes",
            "## Palavras-chave"
        ]

        campos_faltando = []

        for campo in campos_obrigatorios:
            if campo not in conteudo:
                campos_faltando.append(campo)

        if campos_faltando:
            documentos_invalidos.append({
                "arquivo": arquivo.name,
                "faltando": campos_faltando
            })

        documentos.append({
            "arquivo": arquivo.name,
            "conteudo": conteudo
        })

    else:
        arquivos_vazios.append(arquivo.name)

print(f"Documentos encontrados: {len(documentos) + len(arquivos_vazios)}")
print(f"Com conteúdo: {len(documentos)}")
print(f"Vazios: {len(arquivos_vazios)}")
print(f"Estrutura válida: {len(documentos) - len(documentos_invalidos)}")
print(f"Com problemas de estrutura: {len(documentos_invalidos)}")

if arquivos_vazios:
    print("\nArquivos vazios:")

    for arquivo in arquivos_vazios:
        print(f"- {arquivo}")

if documentos_invalidos:
    print("\nProblemas encontrados:")

    for documento in documentos_invalidos:
        print(f"\n- {documento['arquivo']}")

        for campo in documento["faltando"]:
            print(f"  Faltando: {campo}")
            
print(f"\nTotal de chunks gerados: {len(chunks)}")

print("\nExemplo dos primeiros chunks:")

for chunk in chunks[:5]:
    print("\n----------------------------")
    print(f"Arquivo: {chunk['arquivo']}")
    print(f"Chunk: {chunk['chunk_id']}")
    print(chunk["conteudo"][:300])