# Birthdays To Calendar

This Project was created for those who want to remember friends birthdays but don't use facebook anymore.

**NOTE: (20/06/2019) Due to a recent update on Facebook, they removed the option to download the .ICS File. but if you have any other .ics containing Birthdays data, it should work too. But for now, i'm suspend the support for this Repo, feel free to change for your needs.**

With small steps its possible to transfer birthdays from a `.ics` file to Google Calendar.

## Requirements:
- Python 3.X
- A Google account
- An ICS file from your Facebook account (Explanation below about this file)

## Setup Environment:

### Python Environment
Install `pipenv` package if you don't have it. This will help to automatically setup a custom environment for you.
```
pip install pipenv
```

After that, go the the root folder of this project and just enter:
```bash
pipenv install
```

after every thing is done, just enter:
```bash
pipenv shell
```

Everything is set and read to use now!

### Google calendar API
Enable Google Calendar API for your Google Account:
> This step is required to access Google Calendar API services.
- Access [Google Calendar API Quickstart Page](https://developers.google.com/calendar/quickstart/python)
- Go to section 'Step 1: Turn on the Google Calendar API'
- Click the "Enable The Google Calendar API"
- Wait for activation process to be completed
- Click "Download Client Configuration" 
- A file called `credentials.json` will be downloaded.
- Move this file to our project `src` folder.

### Obtaining the .ics file
**NOTE: Facebook disabled this option, buf if you know anywhere else you could get a .ics file, just go on**

Download your Birthdays ICS file from your facebook Events page:
- Access [Facebook Event Page](https://www.facebook.com/events/)
- Scroll Down untill you find this section:

![facebook-birthdays-section](https://github.com/joaoluizn/BirthdaysToCalendar/blob/master/doc/fb-gif.gif)
- Click `Birthdays` to Download friends Birthdays
- Save this file inside project `src` folder and rename it to `events.ics`

## Running:
> Remember to run `pipenv shell`!

- To see possible commands, navigate to project `src` folder and run:
```
python core.py -h
```
### Importing a .ics file:

To import a .ics file just try the following:
```
python core.py --import_birthdays --calendar="Birthdays Calendar" --birthdays_url="path/to/.ics" --visibility="private"
```

This atributes will create a Calendar with name: Birthdays Calendar, importing the events from `.ics` file in `path/to/.ics` setting those events to `private`.

- A Google authentication page will pop-up, just choose the account with Google Calendar API rights previously activated.

- After that, a new Calendar will be created to avoid messing with your Calendar.

- Just Stay cool and wait until the process is over.

- Open your Google Calendar to see it shining with cakes!


### Deleting all Birthdays to Calendar Events from a calendar:

To delete all events added by BirthdaysToCalendar app in a specific Calendar, try the following:

```
python core.py --delete_all_birthdays --calendar="Birthdays Calendar"
```

Now, Just wait untill everything is deleted.

## ToDo:
- Create filter mechanism to remove some people from birthday list.
- Create an user interface to facilitate the process.

## Learned Lessons:
- Some core features envolving friends data access were removed from Facebook API, so it's not that easy to just login with Facebook and get all those data as i thought it would be.

- It's possible to get the ICS file and convert it to CSV them manually import it following the Facebook generated style over the Google Calendar page. I preffer to implement myself and add some custom features.
