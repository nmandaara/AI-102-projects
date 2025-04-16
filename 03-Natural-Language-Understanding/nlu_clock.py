from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta, date, timezone
from dateutil.parser import parse as is_date
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
# Import namespaces


def main():

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
        ai_key = os.getenv("AI_SERVICE_KEY")

        credential = AzureKeyCredential(ai_key)
        # Get user input (until they enter "quit")
        userText = ''
        while userText.lower() != 'quit':
            userText = input('\nEnter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':

                # Create a client for the Language service model
                conversation_client = ConversationAnalysisClient(ai_endpoint, credential)
                # Call the Language service model to get intent and entities
                result = conversation_client.analyze_conversation(
                    task={
                        "kind":"Conversation",
                        "analysisInput": {
                            "conversationItem" : {
                                "participantId" : "1",
                                "id" : "1",
                                "modality" : "text",
                                "language" : "en",
                                "text":userText
                            },
                            "isLoggingEnabled" : False
                        },
                        "parameters":{
                            "projectName" : "test-luis",
                            "deploymentName" : "clock",
                            "verbose":True 
                        }
                    }
                )

                # Apply the appropriate action
                print("query: {}".format(result["result"]["query"]))
                print("project kind: {}\n".format(result["result"]["prediction"]["projectKind"]))

                print("top intent: {}".format(result["result"]["prediction"]["topIntent"]))
                print("category: {}".format(result["result"]["prediction"]["intents"][0]["category"]))
                print("confidence score: {}\n".format(result["result"]["prediction"]["intents"][0]["confidenceScore"]))

                print("entities:")
                for entity in result["result"]["prediction"]["entities"]:
                    print("\ncategory: {}".format(entity["category"]))
                    print("text: {}".format(entity["text"]))
                    print("confidence score: {}".format(entity["confidenceScore"]))
                    if "resolutions" in entity:
                        print("resolutions")
                        for resolution in entity["resolutions"]:
                            print("kind: {}".format(resolution["resolutionKind"]))
                            print("value: {}".format(resolution["value"]))
                    if "extraInformation" in entity:
                        print("extra info")
                        for data in entity["extraInformation"]:
                            print("kind: {}".format(data["extraInformationKind"]))
                            if data["extraInformationKind"] == "ListKey":
                                print("key: {}".format(data["key"]))
                            if data["extraInformationKind"] == "EntitySubtype":
                                print("value: {}".format(data["value"]))
    except Exception as ex:
        print(ex)


def GetTime(location):
    time_string = ''

    # Note: To keep things simple, we'll ignore daylight savings time and support only a few cities.
    # In a real app, you'd likely use a web service API (or write  more complex code!)
    # Hopefully this simplified example is enough to get the the idea that you
    # use LU to determine the intent and entities, then implement the appropriate logic

    if location.lower() == 'local':
        now = datetime.now()
        time_string = '{}:{:02d}'.format(now.hour,now.minute)
    elif location.lower() == 'london':
        utc = datetime.now(timezone.utc)
        time_string = '{}:{:02d}'.format(utc.hour,utc.minute)
    elif location.lower() == 'sydney':
        time = datetime.now(timezone.utc) + timedelta(hours=11)
        time_string = '{}:{:02d}'.format(time.hour,time.minute)
    elif location.lower() == 'new york':
        time = datetime.now(timezone.utc) + timedelta(hours=-5)
        time_string = '{}:{:02d}'.format(time.hour,time.minute)
    elif location.lower() == 'nairobi':
        time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_string = '{}:{:02d}'.format(time.hour,time.minute)
    elif location.lower() == 'tokyo':
        time = datetime.now(timezone.utc) + timedelta(hours=9)
        time_string = '{}:{:02d}'.format(time.hour,time.minute)
    elif location.lower() == 'delhi':
        time = datetime.now(timezone.utc) + timedelta(hours=5.5)
        time_string = '{}:{:02d}'.format(time.hour,time.minute)
    else:
        time_string = "I don't know what time it is in {}".format(location)
    
    return time_string

def GetDate(day):
    date_string = 'I can only determine dates for today or named days of the week.'

    weekdays = {
        "monday":0,
        "tuesday":1,
        "wednesday":2,
        "thursday":3,
        "friday":4,
        "saturday":5,
        "sunday":6
    }

    today = date.today()

    # To keep things simple, assume the named day is in the current week (Sunday to Saturday)
    day = day.lower()
    if day == 'today':
        date_string = today.strftime("%m/%d/%Y")
    elif day in weekdays:
        todayNum = today.weekday()
        weekDayNum = weekdays[day]
        offset = weekDayNum - todayNum
        date_string = (today + timedelta(days=offset)).strftime("%m/%d/%Y")

    return date_string

def GetDay(date_string):
    # Note: To keep things simple, dates must be entered in US format (MM/DD/YYYY)
    try:
        date_object = datetime.strptime(date_string, "%m/%d/%Y")
        day_string = date_object.strftime("%A")
    except:
        day_string = 'Enter a date in MM/DD/YYYY format.'
    return day_string

if __name__ == "__main__":
    main()