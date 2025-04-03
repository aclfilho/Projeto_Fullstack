from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rapidfuzz import process
import pymysql
import os
import logging

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "040115")
DB_NAME = os.getenv("DB_NAME", "teste_intuitive")

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        logging.error(f"Erro na conexão com o banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados")

@app.get("/relevantes")
def operadores_relevantes(limit: int = 5):
    """
    Retorna os operadores mais relevantes com base no maior saldo final.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final
                    FROM demonstracoes_contabeis
                    ORDER BY vl_saldo_final DESC
                    LIMIT %s
                """, (limit,))
                contas = cursor.fetchall()

        if not contas:
            return {"message": "Nenhum operador encontrado."}

        return contas

    except pymysql.MySQLError as e:
        logging.error(f"Erro ao buscar dados: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados: {e}")

# Executar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
