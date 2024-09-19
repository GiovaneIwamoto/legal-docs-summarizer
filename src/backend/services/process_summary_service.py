import os
from services.bedrock_service import get_completion

def process_summary(input_folder, output_folder):
    # Listar todas as subpastas de Textos-Formatados
    subpastas = [subpasta for subpasta in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, subpasta))]

    for subpasta in subpastas:
        input_subpasta_path = os.path.join(input_folder, subpasta)
        output_subpasta_path = os.path.join(output_folder, subpasta)

        # Criar a subpasta em Textos-Resumidos
        if not os.path.exists(output_subpasta_path):
            os.makedirs(output_subpasta_path)

        # Processar os arquivos .txt dentro da subpasta
        for filename in os.listdir(input_subpasta_path):
            if filename.endswith(".txt"):
                input_file_path = os.path.join(input_subpasta_path, filename)
                output_file_path = os.path.join(output_subpasta_path, filename)

                # Ler o conteúdo do arquivo de texto
                with open(input_file_path, "r", encoding="utf-8") as file:
                    text_content = file.read()

                # Gerar o prompt para o Bedrock
                prompt = f"Por favor, forneça um resumo para o seguinte texto:\n\n{text_content}\n\nResumo:"

                # Chamar o modelo Bedrock para gerar o resumo
                try:
                    summary = get_completion(prompt)
                    
                    # Salvar o resumo no arquivo de saída
                    with open(output_file_path, "w", encoding="utf-8") as output_file:
                        output_file.write(summary)

                    print(f"\nResumo gerado para {filename} e salvo em {output_file_path}")
                except Exception as e:
                    print(f"\nErro ao gerar resumo para {filename}: {e}")
