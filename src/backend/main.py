import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from services.ocr_service import process_dataset
from services.process_summary_service import process_summary_individual, process_summary_final
from utils.save_extract_zip_file import save_extract_zip_file

UPLOAD_FOLDER = "uploads"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"]
)

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

    final_summary_path = os.path.join(summarized_folder, "resumo_final.txt")
  
    # Verificar se o resumo final já existe
    if os.path.exists(final_summary_path):
        # Ler o conteúdo do resumo final existente
        with open(final_summary_path, "r", encoding="utf-8") as f:
            final_summary_content = f.read()

        return {
            "detail": "Resumo final resgatado.",
            "final_summary": final_summary_content
        }

    # Processar os textos formatados e gerar os resumos individuais
    process_summary_individual(formatted_folder, summarized_folder)
    
    # Processar os resumos individuais e gerar o resumo final
    process_summary_final(summarized_folder, final_summary_path)
    
    # Conteúdo do resumo final
    with open(final_summary_path, "r", encoding="utf-8") as f:
        final_summary_content = f.read()

    # Retornar o resumo final em formato JSON
    return {
        "detail": "Resumo final gerado com sucesso.",
        "final_summary": final_summary_content
    }
