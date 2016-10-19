import os
from google.cloud import translate
import html.parser as htmlparser

parser = htmlparser.HTMLParser()
client = translate.Client('AIzaSyBt2xPGvDFYLfTy0D_DEm0YAclvjF5Mj50')

#To-do: Confidence checks in language detection
def detectLanguage(message):
    return client.detect_language(message)['language']

def translate(message, target, source=None):
    if source == target:
        return message
    else:
        return parser.unescape(client.translate(message, source_language=source, target_language=target)['translatedText'])

print(translate("Where are you travelling from? Please enter the full address","fr","en"))