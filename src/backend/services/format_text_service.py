import os
from utils.regex_clean_text import regex_clean_text

def format_extracted_text(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each extracted text file
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with open(input_path, "r", encoding="utf-8") as file:
                raw_text = file.read()

            # Call regex util to format text
            formatted_text = regex_clean_text(raw_text)

            # Save the formatted text
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(formatted_text)

            print(f"Formatted text saved to {output_path}")