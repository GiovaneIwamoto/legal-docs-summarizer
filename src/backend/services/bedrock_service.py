# Importação das bibliotecas
import boto3
import json
import os
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura o cliente Bedrock com as credenciais carregadas
bedrock = boto3.client(
    'bedrock-runtime',
    'us-east-1',
    endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

# Cria um corpo de requisição em formato JSON com parâmetros para a solicitação Bedrock
def get_completion(prompt, max_tokens_to_sample=1000):
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens_to_sample,
        "temperature": 1,
        "top_k": 1,
        "top_p": 0.001,
        "stop_sequences": ["\nHuman:"],
        "anthropic_version": "bedrock-2023-05-31"
    })

    # Define informações necessárias para a chamada ao modelo Bedrock
    modelId = 'anthropic.claude-instant-v1'
    accept = 'application/json'
    contentType = 'application/json'

    # Chama o modelo Bedrock com o corpo da requisição
    response = bedrock.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType)

    # Analisa a resposta JSON da chamada ao modelo e extrai a conclusão
    response_body = json.loads(response.get('body').read())
    completion = response_body.get('completion')
    return completion

# Defina a função do prompt, onde passa também o contexto.
def process_obj(obj):
    prompt = f"""
Human: Pegue os dados do arquivo {obj}.
# Defina aqui o seu prompt #
"
Assistant:
"""
    response = get_completion(prompt, 6000)
    return response

# Função que processa o arquivo de entrada e escreve o resultado no arquivo de saída
def process_and_write_output(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file) 
    output_data = [] 

    # Chama a função process_obj para processar cada objeto, converte em JSON e adiciona ao objeto de saida.
    for obj in data:
        result_str = process_obj(obj)  
        result_json = json.loads(result_str)  
        output_data.append(result_json) 

    # Escreve os dados de saída no arquivo de saída, formatando com indentação
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)

# Defina o nome do arquivo de entrada e saida
try:
    input_file = "entrada.json"
    output_file = "saida.json"
    process_and_write_output(input_file, output_file)

# Lida com exceções e exibe uma mensagem de erro em caso de falha
except Exception as e:
    print(f"Erro: {e}")