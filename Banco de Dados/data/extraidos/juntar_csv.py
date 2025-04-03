import os
import pandas as pd

# Obtém o caminho da pasta onde o script está localizado
caminho_pasta = os.path.dirname(os.path.abspath(__file__))

# Lista de arquivos CSV
arquivos = ["1T2023.csv", "2t2023.csv", "3T2023.csv", "4T2023.csv"]

# Lista para armazenar os DataFrames
dfs = []

# Lendo cada arquivo e adicionando na lista
for arquivo in arquivos:
    # Cria o caminho completo para o arquivo
    caminho_arquivo = os.path.join(caminho_pasta, arquivo)
    
    try:
        # Tenta ler o arquivo CSV, ignorando as linhas problemáticas
        df = pd.read_csv(caminho_arquivo, error_bad_lines=False)
        dfs.append(df)
        print(f"Arquivo {arquivo} lido com sucesso.")
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}: {e}")

# Verifique se a lista dfs não está vazia
if len(dfs) > 0:
    # Concatenando todos os DataFrames em um único
    df_final = pd.concat(dfs, ignore_index=True)

    # Salvando o arquivo final na mesma pasta
    caminho_arquivo_final = os.path.join(caminho_pasta, "arquivo_completo.csv")
    df_final.to_csv(caminho_arquivo_final, index=False)

    print(f"Arquivo combinado salvo em: {caminho_arquivo_final}")
else:
    print("Nenhum arquivo foi lido com sucesso.")
