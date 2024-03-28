from pysentimiento import create_analyzer
import transformers

transformers.logging.set_verbosity(transformers.logging.ERROR) 

def analyze_sentiments(texte):
    try :
        result = analyzer_sentimiento.predict(texte)
    except NameError:
        analyzer_sentimiento = create_analyzer(task="sentiment", lang="en")
        result = analyzer_sentimiento.predict(texte)
    return result.probas

def print_result(texte):
    result = analyze_sentiments(texte)
    best_key = max(result, key=result.get)
    return best_key,round(result[best_key]*100, 2)

# print_result("Emma is wearing a pink shirt")