import shutil
from fastapi import UploadFile

# Função para salvar o arquivo na pasta de uploads
def save_upload_file(uploaded_file: UploadFile, destination: str):
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    finally:
        uploaded_file.file.close()