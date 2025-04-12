import os
import requests
import zipfile
from bs4 import BeautifulSoup

# Configurações
URL_ANS = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
PASTA_DOWNLOAD = "anexos"
ARQUIVO_ZIP = "anexos_ans.zip"

def criar_diretorio():
    """Cria o diretório para armazenar os arquivos"""
    try:
        if not os.path.exists(PASTA_DOWNLOAD):
            os.makedirs(PASTA_DOWNLOAD)
    except OSError as e:
        print(f"Erro ao criar diretório: {e}")
        return False
    return True

def encontrar_links_anexos():
    """Encontra os links para os Anexos I e II no site da ANS"""
    try:
        response = requests.get(URL_ANS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links_anexos = []
        
        for link in soup.find_all('a'):
            if 'Anexo I' in link.text or 'Anexo II' in link.text:
                href = link.get('href')
                if href and href.endswith('.pdf'):
                    links_anexos.append(href)
        
        return links_anexos[:2]  # Retorna apenas os dois primeiros
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site: {e}")
        return []

def baixar_pdf(url, nome_arquivo):
    """Faz o download de um arquivo PDF"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        caminho_arquivo = os.path.join(PASTA_DOWNLOAD, nome_arquivo)
        
        with open(caminho_arquivo, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return caminho_arquivo
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo {nome_arquivo}: {e}")
        return None

def criar_zip(arquivos):
    """Cria um arquivo ZIP com os anexos baixados"""
    try:
        with zipfile.ZipFile(ARQUIVO_ZIP, 'w') as zipf:
            for arquivo in arquivos:
                if arquivo and os.path.exists(arquivo):
                    zipf.write(arquivo, os.path.basename(arquivo))
        return True
    except Exception as e:
        print(f"Erro ao criar arquivo ZIP: {e}")
        return False

def main():
    print("Iniciando processo de download...")
    
    if not criar_diretorio():
        return
    
    links = encontrar_links_anexos()
    if not links:
        print("Não foi possível encontrar os links dos anexos.")
        return
    
    arquivos_baixados = []
    for i, link in enumerate(links, 1):
        nome_arquivo = f"Anexo_{i}.pdf"
        caminho = baixar_pdf(link, nome_arquivo)
        if caminho:
            arquivos_baixados.append(caminho)
    
    if arquivos_baixados:
        if criar_zip(arquivos_baixados):
            print(f"Processo concluído! Arquivo {ARQUIVO_ZIP} criado com sucesso.")
        else:
            print("Processo concluído com erros na criação do ZIP.")
    else:
        print("Nenhum arquivo foi baixado com sucesso.")

if __name__ == "__main__":
    main()