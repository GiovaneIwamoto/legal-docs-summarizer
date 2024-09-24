# Importação das bibliotecas
import boto3
import json
import os
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura o cliente Bedrock com as credenciais carregadas
bedrock = boto3.client(
    'bedrock',
    'us-east-1',
    endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

# Cria um corpo de requisição em formato JSON com parâmetros para a solicitação Bedrock
def get_completion(prompt, max_tokens_to_sample=4096):
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens_to_sample,
        "temperature": 0,
        "top_k": 1,
        "top_p": 0.001,
        "stop_sequences": ["\nHuman:"],
    })

    # Define informações necessárias para a chamada ao modelo Bedrock
    modelId = 'anthropic.claude-v2'
    #modelId = 'anthropic.claude-instant-v1'
    
    accept = 'application/json'
    contentType = 'application/json'

    # Chama o modelo Bedrock com o corpo da requisição
    response = bedrock.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType)

    # Analisa a resposta JSON da chamada ao modelo e extrai a conclusão
    response_body = json.loads(response.get('body').read())
    completion = response_body.get('completion')
    return completion

# Função que processa e retorna o resumo de um texto
def process_obj(text_content, type_summary):

    # Aspectos importantes que devem ser considerados no resumo
    key_aspects = f"""
    1. Está sendo julgado um recurso extraordinário ou agravo?
    2. Qual órgão julgador proferiu o acórdão recorrido?
    3. Houve reforma ou confirmação de decisão anterior?
    4. O acórdão recorrido foi proferido por unanimidade de votos ou por maioria?
    5. Quais são os fundamentos apresentados pelo relator?
    6. Qual é a transcrição literal da ementa?
    7. Qual foi o juízo de admissibilidade do recurso extraordinário (admissão ou inadmissão) e quais os seus fundamentos (matéria infraconstitucional, súmula 279, ...)?
    8. O recurso extraordinário foi interposto com fundamento em qual dispositivo constitucional (art. 102, III, a, b, c ou d, da CF)?
    9. Quais os dispositivos indicados como violados e quais os argumentos relevantes do recurso?
    10. Quais os pedidos formulados no recurso?
    11. Existem contrarrazões e quais são os argumentos relevantes do recurso?"""
    
    # Prompt para resumo individual
    if type_summary == "individual":
        print(f"\nUtilizando prompt para resumo individual")
        prompt = f"\n\nHuman: Considerando as perguntas-chave abaixo: \n<perguntas_chave>{key_aspects}\n</perguntas_chave>.\n\nFaça um resumo do texto abaixo dando foco em manter as respostas para as perguntas-chave apresentadas anteriormente: \n<text>\n{text_content}</text>\nO resumo deve ser gerado em formato de texto paragrafado e apresentado direto ao ponto sem introduções.\n\nAssistant:"

    # Prompt para resumo final
    elif type_summary == "final":
        print(f"\nUtilizando prompt para resumo final")
        prompt = f"\n\nHuman: Considerando as perguntas-chave abaixo: \n<perguntas_chave>{key_aspects}\n</perguntas_chave>.\n\n O texto abaixo é um conjunto concatenado de outros resumos, elabore um resumo final dando enfoque em manter as informações que respondem às perguntas-chave mencionadas anteriormente para garantir a inclusão destes pontos relevantes: \n<text>\n{text_content}</text>\nO resumo deve ser gerado em formato de texto paragrafado e apresentado direto ao ponto sem introduções.\n\nAssistant:"
        
    # print(f"\nprompt: {prompt}")

    response = get_completion(prompt, 4096)
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