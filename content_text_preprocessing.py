import re

def clean_text(text: str) -> str:
    text = re.sub(r'\n{2,}', '\n', text)
    sentences = text.split('\n')

    clean_text = ''
    singular_word_list = []

    for sentence in sentences:
        if ' ' not in sentence:
            singular_word_list.append(sentence)
        else:
            clean_text += f'{sentence}\n'

    return clean_text