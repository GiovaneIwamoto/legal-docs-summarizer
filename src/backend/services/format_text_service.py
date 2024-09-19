import os
from utils.regex_clean_text import regex_clean_text

def format_extracted_text(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Processar cada arquivo de texto extraído
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with open(input_path, "r", encoding="utf-8") as file:
                raw_text = file.read()

            # Chama util de regex para formatar texto
            formatted_text = regex_clean_text(raw_text)

            # Salvar o texto formatado
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(formatted_text)

            print(f"Texto formatado salvo em {output_path}")
