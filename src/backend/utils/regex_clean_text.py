import re

def regex_clean_text(text):
    text = re.sub(r'\s{2,}', ' ', text)  # Substitui múltiplos espaços por um único espaço
    text = re.sub(r'([^\n])\n([^\n])', r'\1 \2', text)  # Remove quebras de linha no meio de frases
    text = re.sub(r'\s*\n\s*', '\n', text)  # Remove espaços ao redor de quebras de linha

    return text
