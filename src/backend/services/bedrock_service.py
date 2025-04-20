# Import libraries
import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Bedrock client with loaded credentials
bedrock = boto3.client(
    'bedrock',
    'us-east-1',
    endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

# Create a JSON request body with parameters for the Bedrock request
def get_completion(prompt, max_tokens_to_sample=4096):
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens_to_sample,
        "temperature": 0, # Deterministic
        "top_k": 1, # Most likely token
        "top_p": 0.001, # Cumulative probability
        "stop_sequences": ["\nHuman:"],
    })

    # Define required information for Bedrock model call
    model_id = 'anthropic.claude-v2:1'
    accept = 'application/json'
    content_type = 'application/json'

    # Call Bedrock model with request body
    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type)

    # Parse JSON response from model call and extract completion
    response_body = json.loads(response.get('body').read())
    completion = response_body.get('completion')
    return completion

# Function that processes and returns a text summary
def process_text(text_content, summary_type):

    # Important aspects to be considered in the summary
    key_aspects = """
    # Define the key aspects to be considered in the summary here
    """
    
    # Prompt for individual summary
    if summary_type == "individual":
        prompt = f"\n\nHuman: Produce a textual summary guided by extracting information for the following key concepts:\n\n{key_aspects}\n\nPresent the summary in continuous paragraph format as it deals with a legal document. Here's the text:\n\n<text>\n{text_content}\n</text>\n\nDO NOT PREAMBLE.\n\nAssistant:"

    # Prompt for final summary
    elif summary_type == "final":
        prompt = f"\n\nHuman: Based on the text below which is a set of concatenated summaries:\n\n<text>\n{text_content}\n</text>\n\nRestructure all these individual summaries into a single paragraphed text, preserving all information. DO NOT PREAMBLE. Show only the text in the output, without introductions from your part.\n\nAssistant:"

    response = get_completion(prompt, 4096)
    return response 

# Function that processes the input file and writes the result to the output file
def process_and_write_output(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file) 
    output_data = [] 

    # Call process_text function to process each object, convert to JSON and add to output object
    for item in data:
        result_str = process_text(item)  
        result_json = json.loads(result_str)  
        output_data.append(result_json) 

    # Write output data to output file, formatting with indentation
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)

# Define input and output filenames
try:
    input_file = "input.json"
    output_file = "output.json"
    process_and_write_output(input_file, output_file)

# Handle exceptions and display error message in case of failure
except Exception as e:
    print(f"Error: {e}")
