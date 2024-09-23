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
        print(f"Erro: O arquivo {pdf_path} está vazio ou corrompido.")
        return ""

def process_folder(folder_path, output_folder, log_file):
    # Criar a pasta de saída se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Listar arquivos na pasta
    arquivos = [arquivo for arquivo in os.listdir(
        folder_path) if arquivo.endswith(".pdf")]

    # Processar cada arquivo na pasta
    for arquivo in arquivos:
        pdf_path = os.path.join(folder_path, arquivo)
        texto_extraido = extract_text_from_pdf(pdf_path)

        # Verificar se o texto foi extraído com sucesso antes de criar o arquivo de saída
        if texto_extraido:
            # Gerar o nome do arquivo de saída (trocar extensão para .txt)
            nome_arquivo_saida = os.path.splitext(arquivo)[0] + ".txt"
            caminho_saida = os.path.join(output_folder, nome_arquivo_saida)

            # Escrever o texto extraído em um arquivo de texto
            with open(caminho_saida, "w", encoding="utf-8") as arquivo_saida:
                arquivo_saida.write(texto_extraido)

            print(f"\nTexto extraído do {pdf_path} e salvo em {caminho_saida}")
        else:
            # Adicionar ao arquivo de log
            log_file.write(
                f"Erro: Não foi possível extrair texto de {pdf_path}\n")


def process_dataset(dataset_path):
    # Verificar se a pasta existe
    if not os.path.exists(dataset_path):
        print(f"A pasta {dataset_path} não existe.")
        return

    # Nome do arquivo de log
    log_file_path = os.path.join(dataset_path, "corrompidos.txt")

    # Criar a pasta de saída para os arquivos de texto extraídos
    extracted_output_folder_path = os.path.join(dataset_path, "Textos-Extraidos")
    if not os.path.exists(extracted_output_folder_path):
        os.makedirs(extracted_output_folder_path)

    # Criar a pasta de saída para os arquivos de texto formatados
    formatted_output_folder_path = os.path.join(dataset_path, "Textos-Formatados")
    if not os.path.exists(formatted_output_folder_path):
        os.makedirs(formatted_output_folder_path)

    # Abrir o arquivo de log para escrever
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        # Listar todas as pastas dentro de "dataset"
        subpastas = [subpasta for subpasta in os.listdir(dataset_path)
             if os.path.isdir(os.path.join(dataset_path, subpasta)) 
             and subpasta not in ["Textos-Extraidos", "Textos-Formatados","Textos-Resumidos"]]


        # Processar cada subpasta
        for subpasta in subpastas: # Alterar aqui dependendo da quantidade de subpastas
            subpasta_path = os.path.join(dataset_path, subpasta)
            extracted_subpasta_output_path = os.path.join(extracted_output_folder_path, subpasta)
            formatted_subpasta_output_path = os.path.join(formatted_output_folder_path, subpasta)
            
            # Extrair texto e formatar para cada subpasta
            process_folder(subpasta_path, extracted_subpasta_output_path, log_file)
            format_extracted_text(extracted_subpasta_output_path, formatted_subpasta_output_path)
            
            # Remover a subpasta após o processamento
            shutil.rmtree(subpasta_path) 
