import os
from fastapi import FastAPI, UploadFile, File, HTTPException

from services.ocr_service import process_dataset
from services.process_summary_service import process_summary
from utils.save_extract_zip_file import save_extract_zip_file

UPLOAD_FOLDER = "uploads"

app = FastAPI()

@app.post("/generate_summary/")
async def generate_summary(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser no formato ZIP.")

    # Salvar e extrair o ZIP
    extract_folder = save_extract_zip_file(file, UPLOAD_FOLDER)

    # Processar a pasta extraída com o OCR
    process_dataset(extract_folder)

    # Definir paths para as pastas de textos formatados e resumidos
    formatted_folder = os.path.join(extract_folder, "Textos-Formatados")
    summarized_folder = os.path.join(extract_folder, "Textos-Resumidos")
    os.makedirs(summarized_folder, exist_ok=True)

    # Processar os textos formatados e gerar os resumos individuais
    process_summary(formatted_folder, summarized_folder)

    return {"detail": "Upload e processamento concluídos com sucesso!"}