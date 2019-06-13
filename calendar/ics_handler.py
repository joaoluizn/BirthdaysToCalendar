from icalendar import Calendar
import json

def parse_ics(ics_file):
    parsed_ics = []

    with open(ics_file, 'r') as ics:
        calendar = Calendar.from_ical(ics.read())

        for component in calendar.walk():
            if component.name == "VEVENT":
                print()
                parsed_ics.append(
                    {'summary': str(component.get('SUMMARY')),
                    'start': str(component.get('DTSTART').dt),
                    'uid': str(component.get('UID')), 
                    })
    return json.dumps(parsed_ics, ensure_ascii=False)    
