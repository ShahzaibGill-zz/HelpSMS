import os
from google.cloud import translate
import html.parser as htmlparser

parser = htmlparser.HTMLParser()
client = translate.Client(os.environ['TRANSLATE_KEY'])

#To-do: Confidence checks in language detection
def detectLanguage(message):
    return client.detect_language(message)['language']

def translate(message, target, source=None):
    if source == target:
        return message
    else:
        return parser.unescape(client.translate(message, source_language=source, target_language=target)['translatedText'])