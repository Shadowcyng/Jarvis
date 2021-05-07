import pyttsx3
import datetime
import os
import random
import smtplib
import speech_recognition as sr
import _portaudio
import webbrowser
import wikipedia
from googlesearch import search

from MyDirectory import contacts

engine = pyttsx3.init('sapi5')  # use inbuild voice of windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
_portaudio.initialize()

# TO CHeck the error in the code
# print('cd',pyaudio.pa.get_default_input_device())
# print("count",pyaudio.pa.get_device_count())


def speak(audio):
    ''' It helps to make system speak according to input text '''
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    '''It wishes according to time'''
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour > 12 and hour <= 17:
        speak("Good Afternoon Sir!")
    elif hour > 16:
        speak("Good evening sir!")
    speak("I am Jarvis!. How may I help you ?")


def takeCommand():
    '''It takes microphone input from the user and return spring output'''
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=2)
        print("Listening...")
        audio = r.listen(source, )
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said {query}\n")
        # speak(f"user said {query}")
    except Exception as e:
        print(e)
        print("Say that again please")
        return "None"
    return query


def sendEmail(to, content):
    with open('security.txt', 'r') as f:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            myEmail = f.readline()
            myPassword = f.readline()
            server.login(myEmail, myPassword)  # change with your credenntials
            server.sendmail(
                myEmail, to, f'Subject: Jarvis wants to talk {content}')
            server.close()
        except Exception as e:
            print(e)


        # myEmail = f.readline()
        # myPassword = f.readline()
if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic to execute tasks
        if 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(result)

        elif 'open code' in query or 'open visual studio' in query or 'open vs code' in query:
            codePath = r"C:\Users\Shadowcyng\AppData\Local\Programs\Microsoft VS Code\code.exe"
            os.startfile(codePath)

        elif 'open chrome' in query or 'open google chrome' in query:
            codePath = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            os.startfile(codePath)

        elif 'open youtube' in query:
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            webbrowser.open('www.google.com')

        elif 'open stackoverflow' in query:
            webbrowser.open('www.stackoverflow.com')

        elif 'open facebook' in query:
            webbrowser.open('facebook.com')

        elif query.split(' ')[0].lower() == 'open':
            # webbrowser.open_new_tab(f"{query.split(' ')[1].lower()}.com")
            str = ''
            for index, i in enumerate(query.split(' ')):
                if index != 0:
                    str = str.strip() + i.strip()
            print(str)
            webbrowser.open(f"{str}.com")

        elif 'play music' in query:
            music_dir = 'F:\\Linkin Park\\LP'
            songs = os.listdir(music_dir)
            n = random.choice(range(len(songs)-1))
            os.startfile(os.path.join(music_dir, songs[n]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H: %M : %S")
            speak(
                f"sir,time is {strTime.split(':')[0]} hours, {strTime.split(':')[1]} minutes and {strTime.split(':')[2]} seconds ")

        elif 'the date' in query:
            strDate = datetime.datetime.now().date().strftime('%d %B %Y %A')
            speak(f"sir! date is {strDate} ")

        elif 'send email to' in query or 'send an email to' in query or \
                'send a mail to' in query or 'send email' in query or 'send a mail' in query:
            try:
                name = query.split(' ')[-1]
                if name not in contacts:
                    speak("Whom to send?")
                    name = takeCommand()
                    print(name)
                    name = name.split(' ')[0].lower()
                    if name in contacts:
                        speak("What should I say?")
                        to = contacts[name]
                        content = takeCommand()
                        if content is not None:
                            sendEmail(to, content)
                            speak("Email has been send sir")
                        else:
                            speak("I can send blank emails. Try Again!")
                    else:
                        speak(
                            f"Sorry sir! {name} Did not get match with any contact")
            except Exception as e:
                speak("Sorry sir, I am not able to send this email")

        elif 'google search' in query or 'search' in query or 'google' in query:
            if 'search' in query:
                query.replace("google", '').lower()
            if 'search' in query:
                query.replace("search", '')
            for result in search(query, tld='co.in', lang='en-in', num=10, start=0, stop=1, pause=2.0):
                webbrowser.open(result)
        elif 'thank you' in query:
            speak("You welcome sir, I am always there to help you")
        elif 'i love you' in query or 'love you' in query:
            speak("sorry, i have a boyfriend.")
        elif 'hello jarvis' in query or 'hi jarvis' in query:
            speak("hello sir, what can i do for you?")
        elif 'what can you do for me' in query:
            speak("anything you have trained me to do")