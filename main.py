import speech_recognition as sr
import time
import pywhatkit
import pyttsx3
import webbrowser
import wikipedia
from datetime import date, timedelta, datetime
import sys
import pyautogui
import time
import requests
import operator  # used for math operations
import random  # will be used throughout for random response choices
import os  # used to interact with the computer's directory

# Speech Recognition Constants
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Python Text-to-Speech (pyttsx3) Constants
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


# Wake word in Listen Function
WAKE = "sunday"

# Used to store user commands for analysis
CONVERSATION_LOG = "Conversation Log.txt"

# Initial analysis of words that would typically require a Google search
SEARCH_WORDS = {"who": "who", "what": "what", "when": "when", "where": "where", "why": "why", "how": "how"}

class Sundae:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    # Used to hear the commands after the wake word has been said
    def hear(self, recognizer, microphone, response):
        try:
            with microphone as source:
                print("Waiting for command.")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                # May reduce the time out in the future
                audio = recognizer.listen(source, timeout=5.0)
                command = recognizer.recognize_google(audio)
                s.remember(command)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Network error.")

    # Used to speak to the user
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    # Used to open the browser or specific folders
    def open_things(self, command):
        # Will need to expand on "open" commands
        if command == "open youtube":
            s.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com/")
            pass

        elif command == "open facebook":
            s.speak("Opening Facebook.")
            webbrowser.open("https://www.facebook.com")
            pass

        elif command == "open twitter":
            s.speak("Opening Twitter.")
            webbrowser.open("https://twitter.com")
            pass

        elif command == "open twitter":
            s.speak("Opening Instagram.")
            webbrowser.open("https://www.instagram.com")
            pass

        elif command == "open google":
            s.speak("Opening Google.")
            webbrowser.open("https://www.google.com")
            pass

        elif command == "open my documents":
            s.speak("Opening My Documents.")
            os.startfile("C:/Users/Notebook/Documents")
            pass

        elif command == "open genshin":
            s.speak("Opening Genshin Impact.")
            os.startfile("C:/Program Files/Genshin Impact/launcher.exe")
            pass

        elif command == "open valorant":
            s.speak("Opening Valorant.")
            os.startfile("D:/GAMES/Riot Games/Riot Client/RiotClientServices.exe")
            pass

        else:
            s.speak("I don't know how to open that yet.")
            pass

    # Used to track the date of the conversation, may need to add the time in the future
    def start_conversation_log(self):
        today = str(date.today())
        today = today
        with open(CONVERSATION_LOG, "a") as f:
            f.write("Conversation started on: " + today + "\n")

    # Writes each command from the user to the conversation log
    def remember(self, command):
        with open(CONVERSATION_LOG, "a") as f:
            f.write("User: " + command + "\n")

    # Used to answer time/date questions
    def understand_time(self, command):
        today = date.today()
        now = datetime.now()
        if "today" in command:
            s.speak("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))

        elif command == "what time is it":
            s.speak("It is " + now.strftime("%I") + now.strftime("%M") + now.strftime("%p") + ".")

        elif "yesterday" in command:
            date_intent = today - timedelta(days=1)
            return date_intent

        elif "this time last year" in command:
            current_year = today.year

            if current_year % 4 == 0:
                days_in_current_year = 366

            else:
                days_in_current_year = 365
            date_intent = today - timedelta(days=days_in_current_year)
            return date_intent

        elif "last week" in command:
            date_intent = today - timedelta(days=7)
            return date_intent
        else:
            pass

    # If we're doing math, this will return the operand to do math with
    def get_operator(self, op):
        return {
            '+': operator.add,
            '-': operator.sub,
            'x': operator.mul,
            'divided': operator.__truediv__,
            'Mod': operator.mod,
            'mod': operator.mod,
            '^': operator.xor,
        }[op]

    # We'll need a list to perform the math
    def do_math(self, li):
        # passes the second item in our list to get the built-in function operand
        op = self.get_operator(li[1])
        # changes the strings in the list to integers
        int1, int2 = int(li[0]), int(li[2])
        # this uses the operand from the get_operator function against the two intengers
        result = op(int1, int2)
        s.speak(str(int1) + " " + li[1] + " " + str(int2) + " equals " + str(result))

    # Checks "what is" to see if we're doing math
    def what_is_checker(self, command):
        number_list = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        # First, we'll make a list a out of the string
        li = list(command.split(" "))
        # Then we'll delete the "what" and "is" from the list
        del li[0:2]

        if li[0] in number_list:
            self.do_math(li)

        elif "what is the date today" in command:
            self.understand_time(command)

        else:
            self.use_search_words(command)

    # Checks the first word in the command to determine if it's a search word
    def use_search_words(self, command):
        s.speak("Here is what I found.")
        webbrowser.open("https://www.google.com/search?q={}".format(command))

    # Analyzes the command
    def analyze(self, command):
        try:

            if command.startswith('open'):
                self.open_things(command)
            # USED ONLY FOR YOUTUBE PURPOSES
                if command == "take over the world":
                    s.speak("Skynet activated.")
            #     listening_byte = "T"  # T matches the Arduino sketch code for the blinking red color
            #     ser.write(listening_byte.encode("ascii"))  # encodes and sends the serial byte

            elif command == "introduce yourself":
                s.speak("I am Sunday. I'm a digital assistant made by Riku.")

            elif command == "shutdown the computer":
                s.speak("The computer will shutdown")
                os.system("shutdown /s /t 10")

            elif "play" in command:
                play = command.replace("play", "")
                s.speak("Playing" + play)
                pywhatkit.playonyt(play)

            elif command == "what time is it":
                self.understand_time(command)

            elif command == "close opera":
                s.speak("Closing Opera")
                os.system('TASKKILL /F /IM opera.exe')

            elif command == "close genshin":
                s.speak("Closing Genshin Impact")
                os.system('TASKKILL /F /IM GenshinImpact.exe')

            elif 'take screenshot' in command:
                s.speak("Tell me the name for the file")
                name = command().lower()
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                s.speak("Screenshot saved")

            elif 'volume up' in command:
                s.speak("Increasing the volume")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")

            elif 'volume down' in command:
                s.speak("Decreasing the volume")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")

            elif 'mute' in command:
                s.speak("Muting")
                pyautogui.press("volumemute")

            elif 'refresh' in command:
                s.speak("Refreshing")
                pyautogui.moveTo(1051, 551, 2)
                pyautogui.click(x=1051, y=551, clicks=1, interval=0, button='right')
                pyautogui.moveTo(1120, 605, 1)
                pyautogui.click(x=1120, y=605, clicks=1, interval=0, button='left')

            elif 'scroll down' in command:
                s.speak("Scrolling down")
                pyautogui.scroll(1000)

            elif 'scroll up' in command:
                s.speak("Scrolling up")
                pyautogui.scroll(-1000)

            elif 'maximize this window' in command:
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press('x')

            elif 'google search' in command:
                query = command.replace("google search", "")
                pyautogui.hotkey('alt', 'd')
                pyautogui.write(f"{query}", 0, 1)
                pyautogui.press('enter')

            elif 'youtube search' in command:
                query = command.replace("youtube search", "")
                pyautogui.hotkey('alt', 'd')
                time.sleep(1)
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                time.sleep(1)
                pyautogui.write(f"{query}", 0.1)
                pyautogui.press('enter')

            elif 'open new window' in command:
                pyautogui.hotkey('ctrl', 'n')

            elif 'open incognito window' in command:
                pyautogui.hotkey('ctrl', 'shift', 'n')

            elif 'minimise this window' in command:
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press('n')

            elif 'open history' in command:
                pyautogui.hotkey('ctrl', 'h')

            elif 'open downloads' in command:
                pyautogui.hotkey('ctrl', 'j')

            elif 'previous tab' in command:
                pyautogui.hotkey('ctrl', 'shift', 'tab')

            elif 'next tab' in command:
                pyautogui.hotkey('ctrl', 'tab')

            elif 'open new tab' in command:
                pyautogui.hotkey('ctrl', 't')

            elif 'close tab' in command:
                pyautogui.hotkey('ctrl', 'w')

            elif 'switch tab' in command:
                pyautogui.hotkey('alt', 'tab')

            elif 'close window' in command:
                pyautogui.hotkey('ctrl', 'shift', 'w')

            elif 'clear browsing history' in command:
                pyautogui.hotkey('ctrl', 'shift', 'delete')

            elif command == "how are you":
                current_feelings = ["I'm okay.", "I'm doing well. Thank you.", "I am doing okay."]
                # selects a random choice of greetings
                greeting = random.choice(current_feelings)
                s.speak(greeting)

            elif "weather" in command:
                self.get_weather(command)

            elif "what is" in command:
                self.what_is_checker(command)

            # Keep this at the end
            elif SEARCH_WORDS.get(command.split(' ')[0]) == command.split(' ')[0]:
                self.use_search_words(command)

            else:
                s.speak("I don't know how to do that yet.")

        except TypeError:
            print("Warning: You're getting a TypeError somewhere.")
            pass
        except AttributeError:
            print("Warning: You're getting an Attribute Error somewhere.")
            pass

    # Used to listen for the wake word
    def listen(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print("Listening.")
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    audio = recognizer.listen(source, timeout=5.0)
                    response = recognizer.recognize_google(audio)
                    if response == WAKE:
                        hour = int(datetime.now().hour)
                        if hour >= 0 and hour < 12:
                            s.speak("Good Morning!")

                        elif hour >= 12 and hour < 18:
                            s.speak("Good Afternoon!")

                        else:
                            s.speak("da ngal greetings!")

                        greet_list = ["How can I help you?", "What can I do for you?"]
                        greeting = random.choice(greet_list)
                        s.speak(greeting)
                        return response.lower()
                    else:
                        pass
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Network error.")


s = Sundae()
s.start_conversation_log()
# Used to prevent people from asking the same thing over and over
#previous_response = ""
while True:
    response = s.listen(recognizer, microphone)
    command = s.hear(recognizer, microphone, response)
    s.analyze(command)
    """
    if command == previous_response:
        s.speak("You already asked that. Ask again if you want to do that again.")
        previous_command = ""
        response = s.listen(recognizer, microphone)
        command = s.hear(recognizer, microphone, response)
    
    previous_response = command
    """
