import os
import twilio.twiml
from twilio.rest import TwilioRestClient
from flask import Flask, request, redirect, make_response, session
from translation import detectLanguage, translate
from directions import getDirections
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.environ['SESSION_KEY']
app.permanent_session_lifetime = timedelta(minutes=30)
app.config.from_object(__name__)

@app.route('/', methods=['GET','POST'])
def SMS():
    # Authorization
    twilioNumber = os.environ['TWILIO_NUMBER']
    account_sid = os.environ['TWILIO_SID']
    auth_token = os.environ['TWILIO_AUTH']
    client = TwilioRestClient(account_sid, auth_token)
    fromNumber = request.values.get('From', None)

    message = request.values.get('Body', None)
    # Clearing session. lowercase and source detection
    messageTranslated = translate(request.values.get('Body', None),'en')
    if messageTranslated.lower() == "hello" or messageTranslated.lower() == "hi":
        session.clear()

    #Language detection + Mode Question
    try:
        language = session['language']
    except KeyError:
        language = detectLanguage(message)
        session['language'] = language
        respMessage = translate("What is your mode of transportation? Type 1 for driving, 2 for walking, or 3 for transit.",language, 'en')
        resp = twilio.twiml.Response()
        resp.message(respMessage)
        return str(resp)

    # Mode dection + From address
    try:
        mode = session['mode']
    except KeyError:
        if message == '1':
            session['mode'] = 'driving'
        elif message == '2':
            session['mode'] = 'walking'
        elif message == '3':
            session['mode'] = 'transit'
        else:
            respMessage = translate("What is your mode of transportation? Type 1 for driving, 2 for walking, or 3 for transit",language,"en")
            resp = twilio.twiml.Response()
            resp.message(respMessage)
            return str(resp)
        respMessage = translate("Where are you travelling from? Please enter the full address or Postal Code", language, "en")
        resp = twilio.twiml.Response()
        resp.message(respMessage)
        return str(resp)
    # From location
    try:
        fromLocation = session['fromLocation']
    except KeyError:
        session['fromLocation'] = message
        respMessage = translate("Where are you travelling to? Please enter the full address  or Postal Code", language, "en")
        resp = twilio.twiml.Response()
        resp.message(respMessage)
        return str(resp)

    # To Location
    try:
        toLocation = session['toLocation']
    except KeyError:
        session['toLocation'] = message
        toLocation = session['toLocation']

    directions = getDirections(fromLocation, toLocation, mode, language)
    if len(directions) < 1600:
        directions = [directions[i:i + 1200] for i in range(0, len(directions), 1200)]
        for direction in directions:
            message = client.messages.create(to=twilioNumber, from_=fromNumber, body=direction)
        session.clear()
        return "Done"
    else:
        resp = twilio.twiml.Response()
        resp.message(directions)
        session.clear()
        return str(resp)

if __name__ == "__main__":
    app.run()