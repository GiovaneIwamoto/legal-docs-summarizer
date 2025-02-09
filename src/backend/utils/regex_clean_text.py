import re

def regex_clean_text(text):
    text = re.sub(r'\s{2,}', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'([^\n])\n([^\n])', r'\1 \2', text)  # Remove line breaks in the middle of sentences
    text = re.sub(r'\s*\n\s*', '\n', text)  # Remove spaces around line breaks

    return text
