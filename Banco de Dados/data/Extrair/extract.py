import zipfile
import os
import glob

# Definir os caminhos relativos
zip_folder = "./"  # O script está na mesma pasta dos ZIPs
extract_path = "./extraidos"  # Criará uma pasta "extraidos"

# Garantir que a pasta de extração exista
os.makedirs(extract_path, exist_ok=True)

# Encontrar todos os arquivos ZIP na mesma pasta que o script
zip_files = glob.glob(os.path.join(zip_folder, "*.zip"))

# Extrair cada ZIP
for zip_file in zip_files:
    print(f"Extraindo {zip_file}...")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

print("Todos os arquivos ZIP foram extraídos!")
