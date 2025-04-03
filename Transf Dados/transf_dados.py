# -*- coding: utf-8 -*-
# Script para extrair dados da tabela Rol de Procedimentos - ANS
# Autor: [SEU NOME]
# Data: [DATA]

import pandas as pd
import zipfile
import os
import pdfplumber

def extrair_tabela_ans(pdf_path):
    """
    Função específica para extrair a tabela do Rol de Procedimentos da ANS
    """
    print("Processando o arquivo PDF...")
    
    dados = []
    cabecalho = None
    
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            # Extrai o texto da página para análise
            texto = pagina.extract_text()
            
            # Verifica se é uma página da tabela
            if "Rol de Procedimentos e" in texto:
                print(f"Processando página {pagina.page_number}...")
                
                # Extrai a tabela
                tabela = pagina.extract_table()
                
                if tabela:
                    # A primeira linha válida contém o cabeçalho
                    if not cabecalho:
                        cabecalho = tabela[0]
                        # Padroniza o cabeçalho
                        cabecalho = [col.strip().upper() for col in cabecalho]
                    
                    # Adiciona as linhas de dados (ignorando possíveis cabeçalhos repetidos)
                    for linha in tabela[1:]:
                        if len(linha) == len(cabecalho):  # Verifica se é uma linha válida
                            dados.append(linha)
    
    if not dados:
        print("Não foram encontrados dados na tabela.")
        return None
    
    print(f"Encontradas {len(dados)} linhas de dados.")
    return pd.DataFrame(dados, columns=cabecalho)

def processar_dados(df):
    """Processa e formata os dados extraídos"""
    print("Processando dados...")
    
    # Renomeia colunas conforme solicitado
    df = df.rename(columns={
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial"
    })
    
    # Converte marcadores de cobertura
    for col in ["Seg. Odontológica", "Seg. Ambulatorial"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: "Coberto" if str(x).strip().upper() in ["X", "SIM"] else "")
    
    return df

def salvar_resultados(df, csv_path, zip_path):
    """Salva os resultados em CSV e ZIP"""
    print("Salvando resultados...")
    
    # Salva CSV
    df.to_csv(csv_path, index=False, sep=";", encoding="utf-8-sig")
    
    # Cria ZIP
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))
    
    print(f"Arquivo {zip_path} criado com sucesso!")

def main():
    # Configurações
    pdf_path = "Anexo_1.pdf"
    csv_path = "Rol_de_Procedimentos.csv"
    zip_path = "Teste_Andre.zip"
    
    # Verifica se o arquivo PDF existe
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo {pdf_path} não encontrado!")
        return
    
    # Passo 1: Extrair dados do PDF
    dados_brutos = extrair_tabela_ans(pdf_path)
    if dados_brutos is None:
        print("Não foi possível extrair os dados da tabela.")
        return
    
    # Passo 2: Processar dados
    dados_processados = processar_dados(dados_brutos)
    
    # Passo 3: Salvar resultados
    salvar_resultados(dados_processados, csv_path, zip_path)

if __name__ == "__main__":
    print("=== Início do processamento ===")
    main()
    print("=== Fim do processamento ===")