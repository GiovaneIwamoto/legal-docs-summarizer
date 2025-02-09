import fitz
import os
import shutil
from services.format_text_service import format_extracted_text

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text
    except fitz.fitz.EmptyFileError:
        print(f"Error: File {pdf_path} is empty or corrupted.")
        return ""

def process_folder(folder_path, output_folder, log_file):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List files in folder
    files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

    # Process each file in the folder
    for file in files:
        pdf_path = os.path.join(folder_path, file)
        extracted_text = extract_text_from_pdf(pdf_path)

        # Check if text was successfully extracted before creating output file
        if extracted_text:
            # Generate output filename (change extension to .txt)
            output_filename = os.path.splitext(file)[0] + ".txt"
            output_path = os.path.join(output_folder, output_filename)

            # Write extracted text to a text file
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(extracted_text)
            print(f"\nText extracted from {pdf_path} and saved to {output_path}")
        else:
            # Add to log file
            log_file.write(f"Error: Could not extract text from {pdf_path}\n")

def process_dataset(dataset_path):
    # Check if folder exists
    if not os.path.exists(dataset_path):
        print(f"Folder {dataset_path} does not exist.")
        return

    # Log file name
    log_file_path = os.path.join(dataset_path, "corrupted.txt")

    # Create output folder for extracted text files
    extracted_output_folder_path = os.path.join(dataset_path, "Extracted-Texts")
    if not os.path.exists(extracted_output_folder_path):
        os.makedirs(extracted_output_folder_path)

    # Create output folder for formatted text files
    formatted_output_folder_path = os.path.join(dataset_path, "Formatted-Texts")
    if not os.path.exists(formatted_output_folder_path):
        os.makedirs(formatted_output_folder_path)

    # Open log file for writing
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        # List all folders inside "dataset"
        subfolders = [subfolder for subfolder in os.listdir(dataset_path)
                     if os.path.isdir(os.path.join(dataset_path, subfolder))
                     and subfolder not in ["Extracted-Texts", "Formatted-Texts", "Summarized-Texts"]]

        # Process each subfolder
        for subfolder in subfolders:  # Modify here depending on number of subfolders
            subfolder_path = os.path.join(dataset_path, subfolder)
            extracted_subfolder_output_path = os.path.join(extracted_output_folder_path, subfolder)
            formatted_subfolder_output_path = os.path.join(formatted_output_folder_path, subfolder)

            # Extract text and format for each subfolder
            process_folder(subfolder_path, extracted_subfolder_output_path, log_file)
            format_extracted_text(extracted_subfolder_output_path, formatted_subfolder_output_path)

            # Remove subfolder after processing
            shutil.rmtree(subfolder_path)