from flask import Flask, request, redirect, make_response, session
from translation import detectLanguage, translate
from datetime import timedelta
import langdetect
import twilio.twiml


app = Flask(__name__)
app.secret_key = 'SECRET'
app.permanent_session_lifetime = timedelta(minutes=60)
app.config.from_object(__name__)

@app.route('/', methods=['GET','POST'])
def SMS():
    #Clearing session. lowercase and source detection
    message = translate(request.values.get('Body', None),'en')
    # if message.lower() == "help" or message.lower() == "end":
    #     session.clear()

    #Language detection
    try:
        language = session['language']
    except KeyError:
        language = detectLanguage(message)
        session['language'] = language
        respMessage = translate("What is your mode of transportation? Text 1 for driving...",'en',language)
        resp = twilio.twiml.Response()
        resp.message(respMessage)
        return str(resp)

    # Route detection
    # try:
    #     service = session['mode']
    # except KeyError:
    #     print('do something here')

if __name__ == "__main__":
    app.run()