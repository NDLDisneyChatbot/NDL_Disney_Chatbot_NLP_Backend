
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import json
import dateparser
import datetime
import time
from dateparser.search import search_dates
from textblob import TextBlob
def sentiment_textblob(user_input):
    return TextBlob(user_input).sentiment.polarity

def analyze(user_input):



    client = language.LanguageServiceClient()

    document = types.Document(
        content=user_input,
        type=enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document=document).document_sentiment

    entities = client.analyze_entities(document).entities
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    data = {}

    for entity in entities:
        data[entity_type[entity.type]] = entity.name
    data["sentiment"] = sentiment.score


    user_input = user_input.lower()
    date = search_dates(user_input)

    a_day = 86400 #unix time in a day
    if date is None:
        if "next week" in user_input:
            date = time.time() + (a_day * 7)
        elif "last week" in user_input or "previous week" in user_input:
            date = time.time() - (a_day * 7)
    else:
        date = date[0][1].timestamp()

    data["date"] = date
    data = json.dumps(data)
    return data


