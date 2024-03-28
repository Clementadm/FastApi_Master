from pysentimiento import create_analyzer
import transformers

transformers.logging.set_verbosity(transformers.logging.ERROR) 

def print_result(texte):
    """
    This function analyzes the sentiment of the given text and formats the result for display.
 
    INPUT
            texte (str): The text to be analyzed for sentiment.
 
    OUTPUT
            str: A formatted string indicating the sentiment of the text.
    """
    result = analyze_sentiments(texte)
    best_key = max(result, key=result.get)
    highest_value = round(result[best_key]*100, 2)
    return format_result(best_key, highest_value)
 
 
def analyze_sentiments(texte):
    """
    This function takes a text as input and returns the sentiment of the text.
 
    INPUTS
            texte : str : text to analyze
 
    OUTPUTS
            sentiment : str : sentiment of the text
    """
    transformers.logging.set_verbosity(transformers.logging.ERROR)
    analyzer_sentimiento = create_analyzer(task="sentiment", lang="en")
    result = analyzer_sentimiento.predict(texte)
    return result.probas
 
 
def format_result(best_key, result):
    """
    This function takes the best_key and result and returns a formatted string
 
    INPUT
            best_key : str : key with the highest value
            result : float : highest value
    
    OUTPUT
            str : formatted string
    """
    if best_key == "POS":
        return f"Positive at {result}%"
    elif best_key == "NEG":
        return f"Negative at {result}%"
    else:
        return f"Neutral at {result}%"