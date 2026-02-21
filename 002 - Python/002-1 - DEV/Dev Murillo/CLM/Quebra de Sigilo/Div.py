
# import os
# import re
# import shutil

# # Caminho base das pastas originais
# base_dir = r"C:\Users\mufranca\Desktop\Exemplo QS\Exemplo QS\carta_circular_3454"

# # Caminho base para salvar os resultados ajustados
# output_base = os.path.join(os.path.dirname(base_dir), "Carta Circular 3454 ajustada")

# # Regex para detectar erro (sequências longas de 9s)
# padrao_erro = re.compile(r"9{4,}")

# # Cria a pasta base de saída se não existir
# os.makedirs(output_base, exist_ok=True)

# # Percorre todas as subpastas
# for root, dirs, files in os.walk(base_dir):
#     for file in files:
#         if file.endswith("_ORIGEM_DESTINO.txt"):
#             input_path = os.path.join(root, file)

#             # Cria o caminho equivalente na pasta ajustada
#             relative_path = os.path.relpath(root, base_dir)
#             output_dir = os.path.join(output_base, relative_path)
#             os.makedirs(output_dir, exist_ok=True)

#             # Define os nomes de saída
#             base_name = os.path.splitext(file)[0]
#             output_ok = os.path.join(output_dir, f"{base_name}_OK.txt")
#             output_error = os.path.join(output_dir, f"{base_name}_ERRO.txt")

#             # Lê e separa as linhas
#             with open(input_path, "r", encoding="utf-8") as f:
#                 linhas = [linha.strip() for linha in f if linha.strip()]

#             linhas_erro = [linha for linha in linhas if padrao_erro.search(linha)]
#             linhas_ok = [linha for linha in linhas if not padrao_erro.search(linha)]

#             # Salva os resultados
#             with open(output_error, "w", encoding="utf-8") as f:
#                 f.write("\n".join(linhas_erro))

#             with open(output_ok, "w", encoding="utf-8") as f:
#                 f.write("\n".join(linhas_ok))

#             # Copia o arquivo de INVESTIGADO para a mesma pasta
#             investigado_name = file.replace("_ORIGEM_DESTINO.txt", "_INVESTIGADO.txt")
#             investigado_src = os.path.join(root, investigado_name)
#             if os.path.exists(investigado_src):
#                 shutil.copy(investigado_src, output_dir)

#             print(f"✅ {file} processado com sucesso.")
#             print(f"   → Linhas válidas: {len(linhas_ok)} | Linhas com erro: {len(linhas_erro)}")
#             print(f"   → Pasta destino: {output_dir}")

# print("\n✅ Processamento concluído. Todos os resultados estão em:")
# print(output_base)
import os

# Caminho base da pasta ajustada
ajustada_base = r"C:\Users\mufranca\Desktop\Exemplo QS\Exemplo QS\Carta Circular 3454 ajustada"

# Caminho do arquivo consolidado
output_consolidado = os.path.join(ajustada_base, "Consolidado_Erros.txt")

# Lista para armazenar todas as linhas de erro
todas_linhas_erro = []

# Percorre todas as subpastas em busca dos arquivos *_ERRO.txt
for root, dirs, files in os.walk(ajustada_base):
    for file in files:
        if file.endswith("_ERRO.txt"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                linhas = [linha.strip() for linha in f if linha.strip()]
                # Adiciona um prefixo indicando de qual pasta veio
                for linha in linhas:
                    todas_linhas_erro.append(f"{file} | {linha}")

            print(f"🔍 Erros coletados de: {file_path} ({len(linhas)} linhas)")

# Salva o consolidado
with open(output_consolidado, "w", encoding="utf-8") as f:
    f.write("\n".join(todas_linhas_erro))

print("\n✅ Consolidação concluída!")
print(f"Total de linhas com erro: {len(todas_linhas_erro)}")
print(f"Arquivo consolidado salvo em: {output_consolidado}")
