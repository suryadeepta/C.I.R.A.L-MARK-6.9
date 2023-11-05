from PIL import Image, ImageTk, ImageSequence
import customtkinter as ctk
import tkinter as tk
import threading
import pyttsx3
import speech_recognition as sr
import pyautogui
import time
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import feedparser
import requests
from bs4 import BeautifulSoup
import random
import time
from translate import Translator
from gtts import gTTS
import smtplib
import shutil
import pyperclip
import pyautogui
import webbrowser
from time import sleep
import json
import keyboard
from bardapi import BardCookies


def CookieScrapper():
    webbrowser.open("https://bard.google.com")
    sleep(2)
    pyautogui.click(x=1723, y=64)
    sleep(1)
    pyautogui.click(x=1555, y=242)
    sleep(1)
    pyautogui.click(x=1443, y=104)
    sleep(1)
    keyboard.press_and_release("ctrl + w")

    data = pyperclip.paste()

    try:
        json_data = json.loads(data)
        pass

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")

    SID = "__Secure-1PSID"
    TS = "__Secure-1PSIDTS"
    CC = "__Secure-1PSIDCC"

    SIDValue = next((item for item in json_data if item["name"] == SID), None)
    TSValue = next((item for item in json_data if item["name"] == TS), None)
    CCValue = next((item for item in json_data if item["name"] == CC), None)

    if SIDValue is not None:
        SIDValue = SIDValue["value"]
    else:
        print(f"{SIDValue} not found in the JSON data.")

    if TSValue is not None:
        TSValue = TSValue["value"]
    else:
        print(f"{TSValue} not found in the JSON data.")

    if CCValue is not None:
        CCValue = CCValue["value"]
    else:
        print(f"{CCValue} not found in the JSON data.")

    cookie_dict = {
        "__Secure-1PSID": SIDValue,
        "__Secure-1PSIDTS": TSValue,
        "__Secure-1PSIDCC": CCValue,
    }

    return cookie_dict


directory_name = "Conversations"
if not os.path.exists(directory_name):
    os.makedirs(directory_name)
file_path = os.path.join(directory_name, "conversation_log.txt")
text_file = open(file_path, "a")
text_file.write("\n\n\t\tConversations:\n\n")
text_file.close()


reply_list2 = (
    "Sorry Boss, Can't process. please repeat...",
    "Sorry Boss, don't understood what you said...",
    "Say that again please...",
)

reply2 = random.choice(reply_list2)

language_codes = {
    "afrikaans": "af",
    "albanian": "sq",
    "amharic": "am",
    "arabic": "ar",
    "armenian": "hy",
    "azerbaijani": "az",
    "bengali": "bn",
    "bosnian": "bs",
    "bulgarian": "bg",
    "catalan": "ca",
    "chinese (simplified)": "zh-CN",
    "chinese (traditional)": "zh-TW",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "english": "en",
    "estonian": "et",
    "finnish": "fi",
    "french": "fr",
    "georgian": "ka",
    "german": "de",
    "greek": "el",
    "gujarati": "gu",
    "hebrew": "he",
    "hindi": "hi",
    "hungarian": "hu",
    "icelandic": "is",
    "indonesian": "id",
    "italian": "it",
    "japanese": "ja",
    "kannada": "kn",
    "kazakh": "kk",
    "korean": "ko",
    "latvian": "lv",
    "lithuanian": "lt",
    "macedonian": "mk",
    "malay": "ms",
    "malayalam": "ml",
    "marathi": "mr",
    "mongolian": "mn",
    "nepali": "ne",
    "norwegian": "no",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "punjabi": "pa",
    "romanian": "ro",
    "russian": "ru",
    "serbian": "sr",
    "slovak": "sk",
    "slovenian": "sl",
    "spanish": "es",
    "swedish": "sv",
    "tamil": "ta",
    "telugu": "te",
    "thai": "th",
    "turkish": "tr",
    "ukrainian": "uk",
    "urdu": "ur",
    "vietnamese": "vi",
    "welsh": "cy",
}

global volume
volume = 1
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("volume", volume)


def speak(audio):
    global speaking
    speaking = True
    engine.say(audio)
    engine.runAndWait()
    speaking = False

    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    directory_name = "Conversations"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    file_path = os.path.join(directory_name, "conversation_log.txt")
    with open(file_path, "a", encoding="utf-8") as text_file:
        text_file.write(f"{current_time} - CIRAL: {audio}\n")


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 3 and hour < 11:
        speak("Good Morning!")

    elif hour >= 11 and hour < 15:
        speak("Good noon!")

    elif hour >= 15 and hour < 17:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("Hello Boss, I am kairal, Please tell me how may I help you")


def set_volume(query):
    global volume
    if "set volume to" in query:
        new_volume = query.replace("set volume to", "").strip()
        try:
            volume = float(new_volume)
            engine.setProperty("volume", volume)
            speak(f"Volume has been set to {volume}")
        except ValueError:
            speak("Sorry, I couldn't understand the new volume setting.")


def get_news():
    news_url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(news_url)
    if "entries" in feed:
        headlines = feed.entries[:5]
        speak("Here are the top 5 news headlines:")
        for index, headline in enumerate(headlines):
            speak(f"{index + 1}. {headline.title}")
    else:
        speak(
            "Extreamly Sorry boss, I couldn't fetch the news headlines at the moment."
        )


def get_weather(city):
    try:
        speak("BUt boss, of which city you want to check the weather?")
        try:
            city = takecommand().lower()
        except:
            city = takecommand().lower()

        wttr_url = f"https://wttr.in/{city.replace(' ', '+')}?format=%C with a temparature of %t"

        response = requests.get(wttr_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            weather_info = soup.get_text().strip()

            speak(f"The weather in {city} is {weather_info}.")
        else:
            speak("Sorry, I couldn't fetch the weather information at the moment.")

    except Exception as e:
        speak(f"An error occurred: {e}")


def solve_math_expression(expression):
    try:
        result = eval(expression)
        speak(f"The result of {expression} is {result}")
    except Exception as e:
        speak(f"Sorry, I couldn't solve the math expression due to an error: {e}")


def search_on_youtube(query):
    if "find on youtube" in query:
        ytsearch_query = query.replace("find on youtube", "").strip()

        search_url = f"https://www.youtube.com/results?search_query={ytsearch_query}"
        webbrowser.open(search_url)
        speak(f"Searching YouTube for '{ytsearch_query}'...")
    else:
        speak("No 'find on YouTube' keyword found in the query.")


def open_website(query):
    try:
        if "please open" in query:
            website_name = query.replace("please open", "").strip()

            if not website_name.startswith("https://"):
                website_url = "www." + website_name + ".com"

            webbrowser.open(website_url)
            speak(f"Opening {website_name} in the web browser...")
        else:
            speak("No 'please open' keyword found in the query.")
    except Exception as e:
        speak(f"An error occurred: {e}")


def send_email(receiver_email, subject, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("your gamil address", "Password")

        email_message = f"Subject: {subject}\n\n{message}"

        server.sendmail("your gamil address", receiver_email, email_message)
        server.quit()
        speak("The email is successfully sent boss")
    except Exception as e:
        speak("There is an problem occurred please try one more time")


def update_image(label, image_list, index):
    if index < len(image_list):
        img = image_list[index]
        label.configure(image=img)
        index += 1

        delay = 40
        if speaking:
            delay = 5

        label.after(delay, update_image, label, image_list, index)
    else:
        label.after(0, update_image, label, image_list, 0)


def translate_and_speak():
    recognizer = sr.Recognizer()

    speak("Please speak the text you want to translate.")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)

        speak("Say the target language.")
        target_language_input = takecommand().lower()

        if target_language_input in language_codes:
            target_language = language_codes[target_language_input]
        else:
            speak("No language found. Please try again.")
            return
        translator = Translator(to_lang=target_language)
        translation = translator.translate(user_input)
        translated_text = translation

        directory_name = "Conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        file_path = os.path.join(directory_name, "conversation_log.txt")
        with open(file_path, "a", encoding="utf-8") as text_file:
            text_file.write(f"Translation to {target_language}: {translated_text}\n")

        if target_language == "bn":
            language = target_language
        else:
            language = "en"

        tts = gTTS(
            translated_text,
            lang=language,
        )

        audio_directory = "Audios"
        if not os.path.exists(audio_directory):
            os.makedirs(audio_directory)
        file_path = os.path.join(audio_directory, f"{translated_text}.mp3")
        tts.save(file_path)

        speak("I saved the audio in the Audios folder and will now play the audio.")
        time.sleep(1)
        os.startfile(file_path)

        words = translated_text.split()
        num_words = len(words)
        speaking_rate_wpm = 150
        speaking_time_minutes = num_words / speaking_rate_wpm
        time.sleep(speaking_time_minutes * 60 + 1)

    except Exception as e:
        speak("An error occurred.")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        speak("Recognizing...")
        query = r.recognize_google(audio, language="en-in")

        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        directory_name = "Conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        file_path = os.path.join(directory_name, "conversation_log.txt")
        with open(file_path, "a") as text_file:
            text_file.write(f"{current_time} - Boss: {query}\n")

    except Exception as e:
        speak(reply2)
        return "None"
    return query


recognizer = sr.Recognizer()
engine = pyttsx3.init("sapi5")


def check():
    query = takecommand().lower()
    if "hola amigo" in query:
        speak("Hola boss, please give me some instructions")

    elif "wikipedia" in query:
        speak("Searching in Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            directory_name = "Conversations"
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)
            file_path = os.path.join(directory_name, "conversation_log.txt")
            with open(file_path, "a", encoding="utf-8") as text_file:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                text_file.write(f"{current_time} - Wikipedia results: {results}\n")

            speak(results.encode("utf-8"))
            text_file.close()
        except Exception as e:
            speak("sorry boss, no search results found, try again")
            check()

    elif "set volume to" in query:
        set_volume(query)
        return query
    elif "email" in query:
        speak("whom to send the email?")
        receiver_email = (
            input("Enter the email address of the recipient: ") + "@gmail.com"
        )
        speak("What will be the subject boss?")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)

        subject = r.recognize_google(audio, language="en")
        speak("What do you have to send? , please tell me the message")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        message = r.recognize_google(audio, language="en")
        send_email(receiver_email, subject, message)

    elif "translate" in query:
        translate_and_speak()

    elif "please open" in query:
        open_website(query)

    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif "search" in query:
        search_query = query.replace("search", "").strip()

        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching Google for {search_query}")

    elif "find on youtube" in query:
        search_on_youtube(query)
        time.sleep(3)
        pyautogui.click(x=713, y=314)
        return query

    elif "ask chat gpt" in query:
        ask = query.replace("ask chat gpt", "").strip()
        webbrowser.open(
            "https://chat.openai.com/c/60c112c8-2b6a-4fda-b29b-8ca2fce505f0"
        )
        speak(f"Asking Chad GPT {ask}")
        time.sleep(3)
        pyautogui.write(ask)
        time.sleep(1)
        pyautogui.hotkey("enter")
        time.sleep(5)

    elif "disconnect the bluetooth" in query:
        speak("please wait a few seconds")
        pyautogui.click(x=1713, y=1070)
        time.sleep(2)
        pyautogui.click(x=1671, y=570)
        time.sleep(1)
        pyautogui.click(x=1482, y=1066)
        speak("bluetooth has been disconnected")
        time.sleep(1)

    elif "how are you" in query:
        speak("I am fine ,and always at your service. Boss")

    elif "news" in query:
        get_news()

    elif "weather" in query:
        get_weather("falakata")

    elif "solve" in query:
        expression = query.replace("solve", "").strip()
        solve_math_expression(expression)

    elif "calculate" in query:
        q = query.replace("calculate", "").strip()
        result = eval(q)
        speak(f"The result is {result}")

    elif "roll the music" in query:
        pyautogui.hotkey("win", "s")
        time.sleep(2)
        pyautogui.write("Spotify")
        time.sleep(2)
        pyautogui.press("enter")

        time.sleep(3)

        pyautogui.hotkey("ctrl", "k")
        time.sleep(2)
        pyautogui.write(query.replace("roll the music", "").strip())
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(3)

    elif "pause" in query:
        pyautogui.hotkey("space")

    elif "play the music" in query:
        speak("ok boss")
        pyautogui.hotkey("space")

    elif "start" in query:
        app = query.replace("start", "").strip()
        pyautogui.hotkey("win", "s")
        speak(f"starting {app}")
        time.sleep(2)
        pyautogui.write(app)
        time.sleep(2)
        pyautogui.hotkey("enter")
        time.sleep(2)

    elif "close the program" in query:
        pyautogui.hotkey("alt", "fn", "f4")
        time.sleep(1)

    elif "show me the conversations" in query:
        directory_name = "Conversations"
        file_path = os.path.join(directory_name, "conversation_log.txt")
        text_file = open(file_path, "a")


    elif "clear conversation history" in query:
        if os.path.exists("Conversations"):
            shutil.rmtree("Conversations")

            speak("Previous conversation history has been deleted.")

        else:
            speak("conversation history does not exist.")

    elif "delete all the audio files" in query:
        if os.path.exists("Audios"):
            shutil.rmtree("Audios")

            speak("All audio files has been deleted.")

        else:
            speak("No audio file is there in the folder boss")

    elif "turn off yourself" in query:
        speak("ok boss, BY.")
        directory_name = "Conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        file_path = os.path.join(directory_name, "conversation_log.txt")
        text_file = open(file_path, "a")
        text_file.write("\n\n\t\t\t*************************************\n\n")
        text_file.close()
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")
            exit()
        else:
            exit()

    elif "shutdown" in query:
        speak("Turning of the PC.")
        directory_name = "Conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        file_path = os.path.join(directory_name, "conversation_log.txt")
        text_file = open(file_path, "a")
        text_file.write("\n\n\t\t\t****************xxxxxxxxxxxxxxx****************\n\n")
        text_file.close()
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")
        else:
            os.system("shutdown /s /t 0")
    else:
        speak("Please give me few seconds boss")
        # speak(f"Boss, Give me few seconds to porcess about {query}")
        cookie_dict = CookieScrapper()
        bard = BardCookies(cookie_dict=cookie_dict)
        Reply = bard.get_answer(query)["content"]
        speak(Reply)


def sudo_Analyze():
    speak("Checking all the system files.")
    time.sleep(2)
    speak("Analyzing the data")
    time.sleep(2)
    speak(
        "Your system is completely fine boss. Now you can say hello to me for activation "
    )
    time.sleep(1)


def main():
    wishMe()
    time.sleep(1)
    while True:
        check()


def wake_word():
    sudo_Analyze()
    while True:
        query = takecommand()
        if "hello" in query:
            main()
        elif "no" in query:
            speak("ok boss, see you in a while")
            pyautogui.hotkey("alt", "fn", "f4")


root = ctk.CTk()
root.title("CIRAL")
root.iconbitmap("Assets\LOGO.ico")
root.protocol("WM_DELETE_WINDOW", root.destroy)

speaking = False
image = Image.open("Assets\DO5.gif")
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(image)]


go_thread = threading.Thread(target=wake_word)
go_thread.start()


label = tk.Label(root)
label.config(borderwidth=0)
label.pack()
root.after(0, update_image, label, frames, 0)


root.mainloop()
