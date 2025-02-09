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
    """
    Endpoint to generate a summary from a ZIP file containing documents.

    Args:
        file (UploadFile): The uploaded ZIP file containing documents.

    Returns:
        dict: A dictionary containing the detail message and the final summary content.
    """
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="The file must be in ZIP format.")

    # Save and extract the ZIP file
    extract_folder = save_extract_zip_file(file, UPLOAD_FOLDER)

    # Process the extracted folder with OCR
    process_dataset(extract_folder)

    # Define paths for formatted and summarized text folders
    formatted_folder = os.path.join(extract_folder, "Formatted-Texts")
    summarized_folder = os.path.join(extract_folder, "Summarized-Texts")
    os.makedirs(summarized_folder, exist_ok=True)

    final_summary_path = os.path.join(summarized_folder, "final_summary.txt")
  
    # Check if the final summary already exists
    if os.path.exists(final_summary_path):
        # Read the content of the existing final summary
        with open(final_summary_path, "r", encoding="utf-8") as f:
            final_summary_content = f.read()

        return {
            "detail": "Final summary retrieved.",
            "final_summary": final_summary_content
        }

    # Process the formatted texts and generate individual summaries
    process_summary_individual(formatted_folder, summarized_folder)
    
    # Process the individual summaries and generate the final summary
    process_summary_final(summarized_folder, final_summary_path)
    
    # Read the content of the final summary
    with open(final_summary_path, "r", encoding="utf-8") as f:
        final_summary_content = f.read()

    # Return the final summary in JSON format
    return {
        "detail": "Final summary generated successfully.",
        "final_summary": final_summary_content
    }
