import os
import pandas as pd
import mysql.connector

# Configuração da conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="seu_banco"
)
cursor = conn.cursor()

# Diretório onde estão os arquivos CSV
pasta_csv = "C:/caminho/dos/csv/"

# Lista todos os arquivos CSV na pasta
arquivos = [f for f in os.listdir(pasta_csv) if f.endswith('.csv')]

for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta_csv, arquivo)
    print(f"Importando {caminho_arquivo}...")

    # Carrega o CSV com pandas
    df = pd.read_csv(caminho_arquivo)

    # Insere os dados no MySQL
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO operadoras_saude (coluna1, coluna2, coluna3) VALUES (%s, %s, %s)",
            tuple(row)
        )

    conn.commit()
    print(f"{arquivo} importado com sucesso!")

# Fechar conexão
cursor.close()
conn.close()
