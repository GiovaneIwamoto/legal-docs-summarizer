import zipfile

# Função para extrair o arquivo ZIP
def extract_zip_file(zip_path: str, extract_to: str):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)