from pathlib import Path

pasta_data = Path("../data")

documentos = []
arquivos_vazios = []
documentos_invalidos = []

for arquivo in pasta_data.rglob("*.md"):
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