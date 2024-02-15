import re

def clean_text(text: str) -> str:
    clean_text = re.sub(r'\n{2,}', '\n', text)

    return clean_text