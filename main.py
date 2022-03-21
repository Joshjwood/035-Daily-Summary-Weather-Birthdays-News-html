import smtplib, ssl
import time
from weather_alerts import tomorrow_weather, today_weather, get_weather_data
from news_reports import bbc_today, reuters_today, guardian_today, yesterday_top_3
from birthday_alert import birthday_alert
from privates import *
from email_css import *

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

##############Calendar Reading##################

import httplib2
import os
import datetime

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file

import datetime

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Calendar Reader 1'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_calendar_events():
    """Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    #print('Next 10 events in your calendar:')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    #print(events)
    now = datetime.datetime.now()
    pretty_now = now.strftime("%A %B %d")
    event_text_block = f"<strong>Today is {pretty_now}</strong><br>"
    event_text_block += '<strong>Next 10 events in your calendar:</strong><br><br>'

    if not events:
        event_text_block += 'No upcoming events found.'
    for event in events:
        # Google's json response can be slightly different per event
        # At some point I should figure out why, for now, exceptions will patch it
        try:
            start = event['start']['date']
            start = datetime.datetime.strptime(start, "%Y-%m-%d")
            pretty_time = start.strftime("%I:%M")
            pretty_date = start.strftime("%a %B %d")

            event_text_block += f"<strong>{pretty_date}</strong> - {event['summary']}<br><br>"
            #event_text_block += f"{event['summary']} - {pretty_time} on {pretty_date}<br><br>"


        except:
            start = event['start']['dateTime']
            start = start[:-10]
            try:
                start = datetime.datetime.strptime(start, "%Y-%m-%d")
            except:
                start = start[:-5]
                start = datetime.datetime.strptime(start, "%Y-%m-%d")

            #pretty_time = start.strftime("%I:%M") -- unused
            pretty_date = start.strftime("%a %B %d")

            event_text_block += f"<strong>{pretty_date}</strong> - {event['summary']}<br><br>"
            #event_text_block += f"{event['summary']} - {pretty_time} on {pretty_date}<br><br>"
    return event_text_block




# if __name__ == '__main__':
#     main()

#print(get_calendar_events())

###########End Calendar#############










my_email = MY_EMAIL
password = PASSWORD
my_main_email = MY_MAIN_EMAIL

weather_data = get_weather_data()
news_block = bbc_today() + reuters_today() + guardian_today() + yesterday_top_3()

#########Sending#########

message = email_css_start
# The variable that glues it all together with some html formatting
message += today_weather(weather_data) + "<br>" + tomorrow_weather(weather_data) + f"{birthday_alert()}" + "<br>" + f"{get_calendar_events()}" + news_block + f"<br><br>This email has been brought to you by Josh Wood's automation services, making janky shit work since several months ago.\n \n JWA: Fail upwards"
message += email_css_end

text = message
html = message

message = MIMEMultipart("alternative")
message["Subject"] = f'Morning Report'
message["From"] = my_email
message["To"] = my_main_email

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(my_email, password)
    server.sendmail(
        my_email, my_main_email, message.as_string()
    )
print(f"Email(s) sorted.")