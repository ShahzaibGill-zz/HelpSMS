from googleapiclient.discovery import build

#connect to google translate API
theKey = 'Ask Shabab for this'
service = build('translate', 'v2', developerKey=theKey)

#set up, take from twillo here
inputSentence = 'Salut comment ca va'
inputLanguage =  'fr'
outputLanguage =  'en'
outputSentence = "Well that didn't work"

#translation
translated_sentence = service.translations().list(
	source=inputLanguage,
	target=outputLanguage,
	q=[inputSentence]
	).execute()

outputSentence = translated_sentence['translations'][0]['translatedText']

#processing with translated text (google search)
print(outputSentence)
