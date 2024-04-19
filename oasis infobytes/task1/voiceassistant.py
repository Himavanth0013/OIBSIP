import pyttsx3 as p
import speech_recognition as sp
import os
import webbrowser
import wikipedia
import requests
from bs4 import BeautifulSoup

engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sp.Recognizer()
    with sp.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        print("listening")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            return text.lower()
        except sp.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sp.RequestError:
            speak("Sorry, I'm having trouble accessing the recognition service.")
            return ""

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple options available. Can you please specify?"
    except wikipedia.exceptions.PageError as e:
        return "Sorry, I couldn't find any relevant information on Wikipedia."

def get_ipl_scores():
    url = "https://www.espncricinfo.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scores = soup.find_all('div', class_='match-info match-info-HSB')
    if scores:
        return scores[0].text.strip()
    else:
        return "IPL scores are not available at the moment."

def play_youtube_video(query):
    youtube_url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
    webbrowser.open(youtube_url)

speak("Hello sir, I am your Bheeru. How are you?")

while True:
    text = listen()

    if "bheeru" in text:
        speak("Yes, sir?")
        text = listen()
    
    if "what" in text and "about" in text and "you" in text:
        speak("I am having a good day")

    if "open chrome" in text:
        speak("Opening Chrome...")
        os.system("start chrome")

    if "play video in" in text and "YouTube" in text:
        speak("Sure, what video would you like to watch?")
        video_query = listen()
        play_youtube_video(video_query)

    if "search wikipedia for" in text:
        query = text.replace("search wikipedia for", "").strip()
        speak("Searching Wikipedia...")
        summary = search_wikipedia(query)
        speak(summary)

    if "open website" in text:
        speak("Sure, which website would you like to open?")
        website = listen()
        if "http" not in website:
            website = "http://" + website
        webbrowser.open(website)
    
    if "ipl score" in text:
        speak("Fetching IPL scores...")
        score = get_ipl_scores()
        speak(score)

    speak("What else can I do for you?")
