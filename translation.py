import os
from google.cloud import translate

client = translate.Client('AIzaSyBt2xPGvDFYLfTy0D_DEm0YAclvjF5Mj50')

#To-do: Confidence checks in language detection
def detectLanguage(message):
    return client.detect_language(message)['language']

def translate(message, target, source=None):
    if source == target:
        return message
    else:
        return client.translate(message, source_language=source, target_language=target)['translatedText']

translate("1","en","en")