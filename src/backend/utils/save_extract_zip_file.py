import os
import zipfile
import shutil
from fastapi import UploadFile
from pathlib import Path

# Função para salvar o arquivo na pasta de uploads
def save_upload_file(uploaded_file: UploadFile, destination: str):
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    finally:
        uploaded_file.file.close()

# Função para salvar e extrair o arquivo ZIP
def save_extract_zip_file(file: UploadFile, upload_folder: str) -> str:
    zip_path = os.path.join(upload_folder, file.filename)
    extract_folder = os.path.join(upload_folder, Path(file.filename).stem)

    # Criar a pasta de uploads e a de extração
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(extract_folder, exist_ok=True)

    # Salvar o arquivo ZIP
    save_upload_file(file, zip_path)

    # Extrair o arquivo ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Apagar o arquivo ZIP após a extração
    os.remove(zip_path)

    return extract_folder
