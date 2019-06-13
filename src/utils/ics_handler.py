from icalendar import Calendar
import json

def parse_ics(ics_file):
    parsed_ics = []

    with open(ics_file, 'r') as ics:
        calendar = Calendar.from_ical(ics.read())
        for component in calendar.walk():
            if component.name == "VEVENT":
                parsed_ics.append(
                    {'name': str(component.get('SUMMARY')).split('\'')[0],
                    'start': str(component.get('DTSTART').dt),
                    'uid': str(component.get('UID')).split('@')[0], 
                    })
    return json.dumps(parsed_ics, ensure_ascii=False)
