import argparse
import utils.calendar_handler as cal_handler

from network.connection import stablish_calendar_connection

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="BirthdaysToCalendar, a new approach to import friends birthdays from facebook to Google Calendar.")
parser.add_argument(
    '--import_birthdays', 
    action="store_true", 
    help="""Import your friends birthdays from facebook to Google Calendar.
    Requires:
    [--calendar CALENDAR_NAME], [--facebook_url FACEBOOK_BIRTHDAYS_URL], [--privacy PRIVACY_STATUS]
    """)

parser.add_argument(
    '--calendar',
    type=str,
    metavar=('CALENDAR_NAME'),
    help="""Calendar Name you want to work with.
    
    Used By:
    [--import_birthdays], [--delete_all_birthdays]

    Default:
    If nothing given, a default of name 'Birthdays Calendar' will be created.
    """,
    default="Birthdays Calendar"
)

parser.add_argument(
    '--birthdays_url',
    type=str,
    metavar=('BIRTHDAYS_URL'),
    help="""The URL link that contains your friends birthdays data.
    
    Required By:
    [--import_birthdays]

    More about how to obtain this on README.
    """
)

parser.add_argument(
    '--visibility',
    type=str,
    metavar=('VISIBILITY_STATUS'),
    help="""If you want your events to be public or private.
    
    Options:
        private: The event is public and event details are visible to all readers of the calendar.
        public: The event is private and only event attendees may view event details.

    Required By:
    [--import_birthdays]

    Default: 
        private
    """,
    default='private'
)

parser.add_argument(
    '--delete_all_birthdays', 
    action='store_true',
    help="""All birthdays added by BirthdaysToCalendar for a specific calendar will be deleted
    
    Requires:
    [--calendar CALENDAR_NAME]
    """)

if __name__ == '__main__':
    args = parser.parse_args()

    if args.import_birthdays and args.delete_all_birthdays:
        parser.error('Only one main routine can be executed [--delete_all_birthdays or --import_birthdays]')

    elif args.import_birthdays and not args.delete_all_birthdays:
        if args.calendar and args.birthdays_url and args.visibility:
            conn = stablish_calendar_connection()
            calendar_name = args.calendar
            birthdays_path = args.birthdays_url
            visibility = args.visibility

            if visibility not in ['private', 'public']:
                visibility = 'private'

            birthday_calendar_id = cal_handler.create_birthday_calendar(conn, calendar_name)
            cal_handler.import_ics_to_calendar(conn,birthday_calendar_id, birthdays_path, visibility)
        else:
            parser.error('[--import_birthdays] Requires at least BIRTHDAYS_URL to work')

    elif args.delete_all_birthdays and not args.import_birthdays:
        if args.calendar:
            conn = stablish_calendar_connection()
            calendar_name = args.calendar
            cal_handler.delete_all_birthdays(conn, calendar_name)
        else:
            parser.error('[--delete_all_birthdays] requires a CALENDAR_NAME to delete all birthdays events.')
