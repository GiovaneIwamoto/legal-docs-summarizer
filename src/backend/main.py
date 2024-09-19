import os
import zipfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path

from services.ocr_service import process_dataset
from services.process_summary_service import process_summary
from utils.extract_zip_file import extract_zip_file
from utils.save_upload_file import save_upload_file

UPLOAD_FOLDER = "uploads"

app = FastAPI()

@app.post("/generate_summary/")
async def generate_summary(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser no formato ZIP.")

    # Definir o caminho e criar a pasta uploads
    zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Salvar o arquivo ZIP
    save_upload_file(file, zip_path)

    # Definir o caminho da extração
    extract_folder = os.path.join(UPLOAD_FOLDER, Path(file.filename).stem)
    print("Camiho da pasta extraída:", extract_folder)
    os.makedirs(extract_folder, exist_ok=True)

    # Extrair o arquivo ZIP
    try:
        extract_zip_file(zip_path, extract_folder)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="O arquivo ZIP está corrompido.")

    # Apagar o arquivo ZIP após a extração
    os.remove(zip_path)
    
    # Processar a pasta extraída com o OCR
    process_dataset(extract_folder)

    # Definido paths para as pastas de texto formatado e resumido
    formatted_folder = os.path.join(extract_folder, "Textos-Formatados")
    summarized_folder = os.path.join(extract_folder, "Textos-Resumidos")
    os.makedirs(summarized_folder, exist_ok=True)

    # Processar os textos formatados e gerar os resumos
    process_summary(formatted_folder, summarized_folder)

    return {"detail": "Upload e processamento concluídos com sucesso!"}
