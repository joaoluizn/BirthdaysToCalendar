import datetime
import json

from utils.ics_handler import parse_ics

def create_birthday_calendar(service, calendar_name) -> str:
    calendars = get_calendar_list(service)
    birthday_calendar = None
    
    for calendar_dict in calendars:
        if calendar_name == calendar_dict.get('summary'):
            birthday_calendar = calendar_dict
    
    if not birthday_calendar:
        calendar = {
            'summary': calendar_name,
            'timeZone': 'America/Sao_Paulo',
        }
        response = service.calendars().insert(body=calendar).execute()
        print(f"Calendar created with id: {response.get('id')}")
        return response.get('id')
    else:
        print(f"Calendar '{birthday_calendar.get('summary')}' already exists.")
        return birthday_calendar.get('id') 

def get_calendar_list(service) -> list:
    calendars = []
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendars.append({'summary': calendar_list_entry['summary'], 'id': calendar_list_entry['id']})

        # If there is more than one page of calendars available
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    return calendars

def new_birthday_event(name, date, visibility) -> dict:
    event = {
        'summary': f'{name} 🎂',
        'description': f'Birthday\n\nCreated with BirthdaysToCalendar',
        'start': {
            'date': f'{date}',
        },
        'end': {
            'date': f'{date}'
        },
        'recurrence': [
            'RRULE:FREQ=YEARLY;'
        ],
        'visibility': visibility,
        }
    return event

def add_event_to_calendar(service, calendar_id, event) -> str:
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return f"Event created: {event['summary']}"

def get_next_events(service, calendar_id='primary', event_quantity=10) -> list:
    next_events = []
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {event_quantity} events')
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

def get_all_events(service, calendar_id):
    events_to_return = []
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        for event in events['items']:
            events_to_return.append(event)

        # If there is more than one page of calendars available
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return events_to_return

def delete_all_birthdays(service, calendar_name):
    calendars = get_calendar_list(service)
    birthday_calendar = None
    event_counter = 0
    
    for calendar_dict in calendars:
        if calendar_name == calendar_dict.get('summary'):
            birthday_calendar = calendar_dict

    if birthday_calendar:
        all_events = get_all_events(service, birthday_calendar.get('id'))
        for event in all_events:
            if 'BirthdaysToCalendar' in event.get('description', 'None'):
                event_counter += 1
                print(f'Deleting: {event.get("summary")}  Number: {event_counter}')
                service.events().delete(
                    calendarId=birthday_calendar.get('id'), 
                    eventId=event.get('id')).execute()
        print("All birthdays deleted.")
    else:
        raise ValueError("Calendar Name doesn't exist in your Calendar! Please Verify")

def import_ics_to_calendar(service, calendar_id, ics_path, visibility):
    friends_json = json.loads(parse_ics(ics_path))
    friends_quantity = len(friends_json)
    print(f'This may take a while depending on your friends quantity: {friends_quantity}')
    friends_counter = 0
    for friend in friends_json:
        event = new_birthday_event(
            friend.get('name'), 
            friend.get('start'), 
            visibility)
        friends_counter += 1
        print(f'Adding: {event.get("summary")}  Number: {friends_counter}')
        add_event_to_calendar(service, calendar_id, event)
