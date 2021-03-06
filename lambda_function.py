# -*- coding: utf-8 -*-
import urllib2
import json
from datetime import datetime, timedelta, date

API_BASE="https://waktu-solat-api.herokuapp.com/api/v1/prayer_times.json?negeri=kedah&zon=kuala%20muda"

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.53bc8388-735f-xxxx-82a4-xxxxxxxxxx"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetAllPrayerTimes":
        return get_all_prayer_times()
    elif intent_name == "GetPrayerTime":
        return get_prayer_time(intent)
    elif intent_name == "GetTimeRemaining":
        return get_time_remaining(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "Prayer Time - Done"
    speech_output = "Thank you for using the Prayer Time skill. See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "Prayer Time"
    speech_output = "Welcome to the Alexa Prayer Time skill. " \
                    "At the moment, you can ask me for prayer times in Kuala Muda, Kedah."
    reprompt_text = "Please ask me for prayer times in Kuala Muda, Kedah"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_all_prayer_times():
    session_attributes = {}
    card_title = "All Prayer Times"
    reprompt_text = ""
    should_end_session = False

    response = urllib2.urlopen(API_BASE)
    waktu_solat = json.load(response)

    speech_output = "Prayer times are as follows.\n"

    for prayers in waktu_solat['data']['zon'][0]['waktu_solat']:
        if prayers['name'] == 'subuh':
            speech_output += "Dawn " + prayers['time'] + ",\n"
        elif prayers['name'] == 'isyak':
            speech_output += "Night " + prayers['time'] + ",\n"
        else:
            speech_output += prayers['name'].title() + " " + prayers['time'] + ",\n"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_time_remaining(intent):
    session_attributes = {}
    card_title = "Time Remaining Until Next Prayer"
    speech_output = "I'm not sure which prayer you wanted the time for. Please try again"
    reprompt_text = "I'm not sure which prayer you wanted the time for. Try asking time until Asar for example."
    should_end_session = False

    response = urllib2.urlopen(API_BASE)
    waktu_solat = json.load(response)

    now = datetime.strptime(datetime.utcnow().strftime('%H:%M'), '%H:%M') + timedelta(hours=8)
    now = now.time()

    if "PrayerTime" in intent["slots"]:
        if 'value' not in intent["slots"]["PrayerTime"]:
            for prayers in waktu_solat['data']['zon'][0]['waktu_solat']:
                prayer_time = datetime.strptime(prayers['time'], '%H:%M').time()

                if (now > prayer_time) == False:
                    h,m = get_time_difference(now, prayer_time)
                    speech_output = "You have " + str(h) + " hours and " + str(m) + " minutes until " + prayers['name'].title() + " prayer."
                    reprompt_text = ""
                    break
        else:
            prayer_name = intent["slots"]["PrayerTime"]["value"]
            if prayer_name == 'Subuh':
                prayer_name = 'Dawn'
            if prayer_name == 'Isyak':
                prayer_name = 'Night'
            prayer_code = get_prayer_code(prayer_name.lower())

            if prayer_code != 99:
                prayer_time = datetime.strptime(waktu_solat['data']['zon'][0]['waktu_solat'][prayer_code]['time'], '%H:%M').time()
                h,m = get_time_difference(now, prayer_time)
                card_title = "Time remaining until " + prayer_name.title() + " prayer"
                speech_output = "You have " + str(h) + " hours and " + str(m) + " minutes until " + prayer_name.title() + " prayer."

                reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_prayer_time(intent):
    session_attributes = {}
    card_title = "Prayer Time"
    speech_output = "I'm not sure which prayer you wanted the time for. Please try again"
    reprompt_text = "I'm not sure which prayer you wanted the time for. Try asking Asar for example."
    should_end_session = False

    response = urllib2.urlopen(API_BASE)
    waktu_solat = json.load(response)

    if "Prayer" in intent["slots"]:
        prayer_name = intent["slots"]["Prayer"]["value"]
        if prayer_name == 'Subuh':
            prayer_name = 'Dawn'
        if prayer_name == 'Isyak':
            prayer_name = 'Night'
        prayer_code = get_prayer_code(prayer_name.lower())

        if prayer_code != 99:
            card_title = prayer_name.title() + " prayer time."
            speech_output = "The time for " + prayer_name + " prayer is " + waktu_solat['data']['zon'][0]['waktu_solat'][prayer_code]['time']

            reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_prayer_code(prayer_name):
    return {
        "imsak": 0,
        "dawn": 1,
        "syuruk": 2,
        "zohor": 3,
        "asar": 4,
        "maghrib": 5,
        "night": 6
    }.get(prayer_name, 99)

def get_time_difference(now, after):
    countdown = datetime.combine(date.today(), after) - datetime.combine(date.today(), now)
    m,s = divmod(countdown.seconds, 60)
    h,m = divmod(m, 60)
    return h,m

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
