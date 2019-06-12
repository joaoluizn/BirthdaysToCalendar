from connection import stablish_calendar_connection
from pprint import pprint
import datetime

def create_calendar(service):
    calendar = {
        'summary': 'BirthdaysToCalendar-Test',
        'timeZone': 'America/Sao_Paulo',
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    return created_calendar['id']

def get_next_events(service, calendar_id='primary', event_quantity=10) -> list:
    next_events = []
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(
        calendarId=calendar_id, 
        timeMin=now, 
        maxResults=event_quantity, 
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        next_events.append((event['summary'], start))

    return next_events

def get_calendar_list(service) -> list:
    calendars = []
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendars.append((calendar_list_entry['summary'], calendar_list_entry['id']))
        
        # If there is more than one page of calendars available
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    return calendars

def add_event_to_calendar(service, calendar_id, event):
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    # {event.get('htmlLink')}
    print(f"Event created: {event['htmlLink']}")

if __name__ == '__main__':
    conn = stablish_calendar_connection()
    calendars = get_calendar_list(conn)
    birthday_calendar_id = None
    for cal in calendars:
        if 'BirthdaysTocalendar' in cal[0]:
            birthday_calendar_id = cal[1]
            print(get_next_events(conn, birthday_calendar_id))

    # Create Event
    event = {
        'summary': 'Evandro Rosas 🎂',
        'description': 'Aniversário',
        'start': {
            'date': '2019-10-14',
        },
        'end': {
            'date': '2019-10-14'
        },
        'recurrence': [
            'RRULE:FREQ=YEARLY;'
        ],
        'visibility': 'private',
    }

    add_event_to_calendar(conn, birthday_calendar_id, event)