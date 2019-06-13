import json

import utils.calendar_handler as cal_handler
from network.connection import stablish_calendar_connection
from utils.ics_handler import parse_ics


if __name__ == '__main__':
    calendar_name = 'Birthdays T1'

    # Creating Connecton with Google Calendar API
    conn = stablish_calendar_connection()

    # Create birthday calendar if needed
    birthday_calendar_id = cal_handler.create_birthday_calendar(conn, calendar_name)

    friends_json = json.loads(parse_ics('events.ics'))

    # TODO: Filter people before add final list. 

    friends_quantity = len(friends_json)
    print(f'This may take a while depending on your friends number: {friends_quantity}')
    
    added_quantity = 0
    for friend in friends_json:
        event = cal_handler.new_birthday_event(
            friend.get('name'), 
            friend.get('start'), 
            friend.get('uid'))
        cal_handler.add_event_to_calendar(conn, birthday_calendar_id, event)
        added_quantity += 1

        if added_quantity % 20 == 0 or added_quantity == friends_quantity:
            print(f'Progress: {added_quantity}/{friends_quantity}: {(added_quantity/friends_quantity)*100:.2f}%')
