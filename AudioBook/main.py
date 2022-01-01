import speech_recognition as sr
import pyttsx3  # pip install pyttsx3==2.71
import PyPDF2
import os
import datetime
from datetime import date
import time
import re


speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[4].id)
# speaker.setProperty('rate', 100)


# Speak method to give voice output
def speak(audio):
    try:
        speaker.say(audio)
        speaker.setProperty('rate', 200)
        speaker.runAndWait()
    except Exception as e:
        print(e)
        speak("I am afraid I can't understand you sir!")


# Take voice command from user
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='en-in')
        print("User said:", command)
    except Exception as e:
        print(e)
        speak("I am sorry, I can't understand you sir!")
        command = take_command()
    return command


# Greetings
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Sir! I am your personal AudioBook")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir! I am your personal AudioBook")
    elif 18 <= hour < 22:
        speak("Good Evening Sir! I am your personal AudioBook")
    else:
        speak("It's been too late to stay awake Sir!")
    speak("How can I help u?")


# Extract integer from string, when getting page number from voice input
def extract_integer(a):
    number = 0
    for word in a.split():
        if word.isdigit():
            number = int(word)
    return number


# Get PDF files from the directory given by user
def get_pdfs(path):
    files_list = os.listdir(path)
    pdf_list = []
    for file in files_list:
        if file.endswith(('.pdf', '.PDF')):
            pdf_list.append(file)

    return pdf_list


# Find the pdf user want to read, return a boolean value based on found or not
def find_pdf(user_cmd, list_pdf):
    res = 0
    for item in list_pdf:
        if user_cmd == item.lower().split('.')[0]:
            res = 1
            return res, item
    return res, list_pdf


# Read pdf method
def read_book():
    speak("Entering reading mode... Give a directory path sir...")
    dir_path = input("Path: ")
    speak("Opening the specified path..")
    dir_pdfs = get_pdfs(dir_path)

    # Printing all the available pdfs to show the user
    for pdf in dir_pdfs:
        print(pdf)
    speak(f"I found {len(dir_pdfs)} pdf in this directory, which one you want to read?")
    command = take_command().lower()

    found, found_pdf = find_pdf(command, dir_pdfs)

    if found:
        speak("Working on it Sir...")
        speak(f"Opening {found_pdf}")
        os.startfile(f"{dir_path}\{found_pdf}")
        f = open(f"{dir_path}\{found_pdf}", 'rb')
        pdf_reader = PyPDF2.PdfFileReader(f)
        total_pages = pdf_reader.numPages
        speak(f"This pdf contains {total_pages} pages.")
        speak("Do you want to continue reading sir?")
        command = take_command().lower()
        if bool(re.search(r'\bno\b', command)) or bool(re.search(r'\bexit\b', command)):
            speak("Exiting reading mode Sir!")
            os.system("taskkill /f /im msedge.exe")
            f.close()
        if bool(re.search(r'\byes\b', command)) or bool(re.search(r'\bcontinue\b', command)):
            speak("Which page should I read Sir?")
            command = take_command()
            page_no = extract_integer(command)
            speak("Opening page " + str(page_no))
            page = pdf_reader.getPage(page_no - 1)
            text = page.extractText()
            speak(text)
            os.system("taskkill /f /im msedge.exe")
    else:
        speak("I am sorry! I cannot find the pdf in your given path sir!")


if __name__ == "__main__":
    print("WELCOME!")
    wish_me()
    while True:
        respond = take_command().lower()
        if bool(re.search(r'\bhello\b', respond)) or bool(re.search(r'\bhi\b', respond)):
            speak("Hello Sir! Nice to have you back..")
        elif bool(re.search(r'\bdate\b', respond)):
            today = date.today()
            date_today = today.strftime("%A %B %d, %Y")
            speak("Its" + date_today)
        elif bool(re.search(r'\btime\b', respond)):
            current_time = time.strftime("%I:%M %p")
            speak("Its" + current_time)
        elif bool(re.search(r'\benter\b', respond)) or bool(re.search(r'\bread\b', respond)):
            read_book()
        elif bool(re.search(r'\bexit\b', respond)) or bool(re.search(r'\bsleep\b', respond)):
            speak("As usual its a great pleasure watching you work. Have a nice day Sir.")
            exit()

