#!/usr/bin/env python
# coding: utf-8

# ![cfdf7ee0-bb65-4ba9-9341-a893835a149d_200x200.png](attachment:cfdf7ee0-bb65-4ba9-9341-a893835a149d_200x200.png)

# In[ ]:


#libraries
import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import lxml
import urllib
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup as soup
#from urllib import urlopen
import wikipedia
import random
#import tekore as te
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import strftime


# In[17]:


#E.R.I.C main 
def jarvisResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)
def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Speak...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands 
    #if unrecognizable speech is received
    except sr.UnknownValueError:
        jarvisResponse("Sorry?")
        #print('....')
        command = myCommand();
    return command
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        # print(dirs)
        if dir!= '.git':
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))


# In[2]:


#Duties of E.R.I.C
def assistant(command):
    "if statements for executing commands"
#open subreddit Reddit
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        jarvisResponse('The Reddit content has been opened for you Sir.')
    elif 'tata' in command:
        jarvisResponse('Bye bye Sir. Have a nice day')
        sys.exit()
    elif 'thank you' in command:
        jarvisResponse('Bye bye Sir. Have a nice day')
        sys.exit()    
#open website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            jarvisResponse(f'The website, {domain}, you have requested has been opened for you Sir.')
        else:
            pass
#greetings
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if 6 <= day_time < 12:
            jarvisResponse('Good morning. Hope you got some Sleep sir. And Sir, if you want to list my responsibilities, please say jobs!')
        elif 12 <= day_time < 18:
            jarvisResponse('Good afternoon. Jai Mata di, lets rock. And Sir, if you want to list my responsibilities, please say jobs!')
        elif 18 <= day_time < 21:
            jarvisResponse('Good evening. Jai Mata di, lets rock. And Sir, if you want to list my responsibilities, please say jobs!')
        else:
            jarvisResponse('Good Night. Please try to get some sleep Sir!')     
    elif 'jobs' in command:
        jarvisResponse("""
        My Responsibilities are:
            1.To greet you (command: Hello)
            2.To give you the current news(command: news for today)
            3.To respond with multiple jokes(command: joke)
            4.To open native apps(command: launch app)
            5.Open any website (command: Open website.com)
            6.To open SubReddits (command: open reddit subReddit)
            7.Send email, I will ask questions such as recipient name and content.(command: Send email)
            8.Tell you about Current weather conditions(command: Current weather in {weather})
            9.Play a video you desire(command: play me a video)
            10.To search for things on wikipedia(command: about topic)
            11.To respond with the current time (command: time)
            12.To leave you when you ask me to(command: bye)
            13.To Manipulate folders like create a new folder, remove folder etc.
        """)
#joke
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            jarvisResponse(str(res.json()['joke']))
        else:
            jarvisResponse('oops!I ran out of jokes')
#top stories from google news
    elif 'news' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"lxml")
            news_list=soup_page.findAll("item")
            for news in news_list[:10]:
                jarvisResponse(news.title.text)#encode('utf-8'))
        except Exception as e:
                print(e)
#current weather
    elif 'current weather' in command: #NW
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            jarvisResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
#time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        jarvisResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))
    elif 'email' in command:
        jarvisResponse('Who is the recipient?')
        recipient = myCommand()
        if ' ' in recipient:
            jarvisResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('your_email_address', 'your_password')
            mail.sendmail('sender_email', 'receiver_email', content)
            mail.close()
            jarvisResponse('Email has been sent successfuly. You can check your inbox.')
        else:
            jarvisResponse('I don\'t know what you mean!')
#launch any application
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
        jarvisResponse(f'I have launched the {appname} application')
#play youtube song
    elif 'music' in command: #NW
        #path = '/Users/Apple/Documents/videos/'
        #folder = path
        #for the_file in os.listdir(folder):
        #    file_path = os.path.join(folder, the_file)
        #    try:
        #        if os.path.isfile(file_path):
        #            os.unlink(file_path)
        #    except Exception as e:
        #        print(e)
        jarvisResponse('What song shall I play Sir?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urllib.request.urlopen(url)
            html = response.read()
            soup1 = soup(html,"lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
                    url = url_list[0]
                    ydl_opts = {}
                    os.chdir(path)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                vlc.play(path)
        if flag == 0:
            jarvisResponse('I have not found anything in Youtube ')
#change wallpaper
    elif 'change wallpaper' in command: #NW
        folder = '/Users/Apple/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key #pic from unspalsh.com
        f = urllib.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.urlretrieve(photo, "/Users/Apple/Documents/wallpaper/a") # Location where we download the image to.
        subprocess.call(["killall Dock"], shell=True)
        jarvisResponse('wallpaper changed successfully')
#askme anything
    elif 'about' in command:
        reg_ex = re.search('about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group() #(1)
                ny = wikipedia.page(topic)
                jarvisResponse(ny.content[:1000])#.encode('utf-8')) #\n added
        except Exception as e:
                print(e)
    #elif 'greet' in command:
    #    jarvisResponse('Greetings Sweeney pie!')
    elif 'awesome' in command:
        jarvisResponse('Thank you sir!!!')
    #FILE MANIPULATION COMMANDS
    elif 'secret folder' in command:
        jarvisResponse('Working on a secret project are we sir?')
        proj = myCommand()
        if 'yes' in proj:
            os.mkdir('Desktop/NewProject')
            os.rename('Desktop/NewProject', 'Desktop/.NewProject')
            jarvisResponse('Secret Directory created sir!')
        elif 'no' in proj:
            jarvisResponse('Changing your mind sir? Sure.')
        elif 'delete' in proj:
            os.rmdir("Desktop/.NewProject")  
            os.chdir("..")  
            os.rmdir(".NewProject")  
            jarvisResponse('Directory Deleted Sir!')
        else:
            jarvisResponse('i dont understand sir')
    elif 'create folder' in command:
        os.mkdir('Desktop/NewProject')
        jarvisResponse('New Directory Created Sir!')
    elif 'remove folder' in command:
        jarvisResponse("Are you sure you want to delete it?")
        dele = myCommand()
        if 'yes' in dele:
            os.rmdir("Desktop/NewProject")  
            os.chdir("..")  
            os.rmdir("NewProject")  
            jarvisResponse('Directory Deleted Sir!')
        elif 'no' in dele:
            jarvisResponse("I am not deleting the Directory sir")
    elif 'list all files' in command:
        jarvisResponse('The following are the files sir!')
        startpath = os.getcwd()
        list_files(startpath)
    elif 'list files' in command:
        jarvisResponse('The following are the files in the Directory sir!')
        startpath = os.getcwd()
        list_files('Desktop/ChallengeDB')
    elif 'desktop files' in command:
        jarvisResponse('The following are the files in the Directory sir!')
        print(os.listdir('Desktop'))
    elif 'test' in command: #NW
        reg_ex = re.search('test (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".py"
            subprocess.Popen(["open", "-n", "/Desktop/" + appname1], stdout=subprocess.PIPE)
        jarvisResponse(f'I have launched the {appname} application')
    elif 'play' in command: #NW
        lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        results = spotify.artist_top_tracks(lz_uri)

        for track in results['tracks'][:10]:
            print('track    : ' + track['name'])
            print('audio    : ' + track['preview_url'])
            print('cover art: ' + track['album']['images'][0]['url'])
            print()


# In[1]:


print('E.R.I.C = Enhanced Realtime Intelligent Computer, by Anuraag Rath' + "\n")
jarvisResponse('Oh Hello Sir! Eric here. How is your day going? I am doing fine. I am at your Service sir!! Please say jobs so that i could list you my various duties')
#loop to continue executing multiple commands
while True:
    assistant(myCommand())


# In[ ]:




