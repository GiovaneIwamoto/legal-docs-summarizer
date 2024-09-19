import fitz
import os

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

            print(f"Texto extraído do {pdf_path} e salvo em {caminho_saida}")
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

    # Criar a pasta de saída para os arquivos de texto
    output_folder_path = os.path.join(dataset_path, "Textos-Extraidos")
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Abrir o arquivo de log para escrever
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        # Listar todas as pastas dentro de "dataset"
        subpastas = [subpasta for subpasta in os.listdir(
            dataset_path) if os.path.isdir(os.path.join(dataset_path, subpasta))]

        # Processar cada subpasta
        for subpasta in subpastas[:-1]:
            subpasta_path = os.path.join(dataset_path, subpasta)
            subpasta_output_path = os.path.join(output_folder_path, subpasta)
            process_folder(subpasta_path, subpasta_output_path, log_file)