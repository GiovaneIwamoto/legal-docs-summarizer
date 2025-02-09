import os
import zipfile
import shutil
from fastapi import UploadFile
from pathlib import Path

def save_upload_file(uploaded_file: UploadFile, destination: str):
    """
    Save the uploaded file to the specified destination.

    Args:
        uploaded_file (UploadFile): The file uploaded by the user.
        destination (str): The path where the file should be saved.
    """
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    finally:
        uploaded_file.file.close()

def save_extract_zip_file(file: UploadFile, upload_folder: str) -> str:
    """
    Save and extract the contents of a ZIP file.

    Args:
        file (UploadFile): The ZIP file uploaded by the user.
        upload_folder (str): The folder where the file should be saved and extracted.

    Returns:
        str: The path to the folder where the contents of the ZIP file were extracted.
    """
    zip_path = os.path.join(upload_folder, file.filename)
    extract_folder = os.path.join(upload_folder, Path(file.filename).stem)

    # Create the upload and extraction folders
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(extract_folder, exist_ok=True)

    # Save the ZIP file
    save_upload_file(file, zip_path)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Delete the ZIP file after extraction
    os.remove(zip_path)

    return extract_folder
