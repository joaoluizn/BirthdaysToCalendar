# Birthdays To Calendar

This Project was created for those who want to remember friends birthdays but don't use facebook anymore.

**NOTE: (20/06/2019) Due to a recent update on Facebook, they removed the option to download the .ICS File. but if you have any other .ics containing Birthdays data, it should work too. But for now, i'm suspend the support for this Repo, feel free to change for your needs.**

With small steps its possible to transfer birthdays from Facebook to Google Calendar.

## Requirements:
- Python 3.X
- A Google account
- An ICS file from your Facebook account (Explanation below about this file)

## Setup:
Create a virtual environment wherever you want:
> Strongly recommend a folder on your home directory to store your envs.
```bash
python -m venv <your_env_name>
```

Activate your virtual environment:
```bash
$ source <your_env_name>/bin/activate
```

While in project root folder, Install Python dependencies on your virtual env:
```bash
pip install -r requirements.py
```

Enable Google Calendar API for your Google Account:
> This step is required to access Google Calendar API services.
- Access [Google Calendar API Quickstart Page](https://developers.google.com/calendar/quickstart/python)
- Go to section 'Step 1: Turn on the Google Calendar API'
- Click the "Enable The Google Calendar API"
- Wait for activation process to be completed
- Click "Download Client Configuration" 
- A file called `credentials.json` will be downloaded.
- Move this file to our project `src` folder.

Download your Birthdays ICS file from your facebook Events page:
- Access [Facebook Event Page](https://www.facebook.com/events/)
- Scroll Down untill you find this section:

![facebook-birthdays-section](https://github.com/joaoluizn/BirthdaysToCalendar/blob/master/doc/fb-gif.gif)
- Click `Birthdays` to Download friends Birthdays
- Save this file inside project `src` folder and rename it to `events.ics`

## Running:
> Remember to activate your virtual env!

- Navigate to project `src` folder and run:
```
python core.py
```

- A Google authentication page will pop-up, just choose the account with Google Calendar API rights previously activated.

- After that, a new Calendar will be created to avoid messing with your Calendar.

- Just Stay cool and wait until the process is over.

- Open your Google Calendar to see it shining with cakes!

> All created events are privates and only visible to the owner. Events property creation are found inside `calendar_handler` file.

## ToDo:
- Apply ArgParser to enhance CLI.
- Create filter mechanism to remove some people from birthday list.
- Create an user interface to facilitate the process.

## Learned Lessons:
- Some core features envolving friends data access were removed from Facebook API, so it's not that easy to just login with Facebook and get all those data as i thought it would be.

- It's possible to get the ICS file and convert it to CSV them manually import it following the Facebook generated style over the Google Calendar page. I preffer to implement myself and add some custom features.
