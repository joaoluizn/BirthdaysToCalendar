import datetime

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

def new_birthday_event(name, date, uid) -> dict:
    event = {
        'summary': f'{name} 🎂',
        'description': f'Aniversário\nid: {uid}.',
        'start': {
            'date': f'{date}',
        },
        'end': {
            'date': f'{date}'
        },
        'recurrence': [
            'RRULE:FREQ=YEARLY;'
        ],
        'visibility': 'private',
        }
    return event

def add_event_to_calendar(service, calendar_id, event) -> str:
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return f"Event created: {event['summary']}"

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
