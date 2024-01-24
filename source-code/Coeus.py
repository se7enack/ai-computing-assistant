#!/usr/bin/env python3

import requests
import subprocess
import easygui 
import os
import threading
from gtts import gTTS
import time
from pygame import mixer
# pip3 install requests easygui thread6 pygame gtts chardet

title = "COEUS"
getimagemodel = "dall-e-3"
getimageurl = "https://api.openai.com/v1/images/generations" 
getinfomodel = "gpt-3.5-turbo-instruct"
getinfourl = "https://api.openai.com/v1/completions"
home = os.path.expanduser('~')
apikeyfile = f"{home}/.api.key"


def talkbox(x):    
    file = f"{home}/.aireply.mp3"
    tts = gTTS(x)
    tts.save(file)
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)


def result(ai):
    choices = ["OK", "Read it to me"]
    ans = easygui.buttonbox(ai, title, choices)
    if ans == "Read it to me":
        x = threading.Thread(target=talkbox, args=(ai,))
        x.start()
    exit(0)


def basicask(q):
    try:
        payload = easygui.enterbox(q)
        happy = bool(payload)
        if happy == True:
            return payload
        else:
            exit(0)
    except AttributeError:
        exit(0)


def asktype():
    with open(apikeyfile) as f:
        apikey = f.read()    
    message = "What are you looking to do?"
    choices = ["Ask AI a Question", "Ask AI to Generate an Image", "Exit"]
    output = easygui.buttonbox(message, title, choices)
    if output == "Ask AI a Question":
        ccc = basicask("What would you like to ask AI?")
        ai = getinfo(apikey, ccc)
        result(ai)
    elif output == "Ask AI to Generate an Image":
        ccc = basicask("Which image would you like AI to generate?")
        ai = getimage(apikey, ccc)
        choices = ["OK"]
        easygui.buttonbox(ai, title, choices)
        exit(0)
    else:
        exit(0)


def starthere():
    if os.path.exists(apikeyfile):
        readkey()
    else:
        apikey = createkey("Enter an API Key to get started")      
        with open(apikeyfile, 'w') as file:
            try:
                file.write(apikey)
            except TypeError:
                exit(0)
    asktype()
                

def readkey():
    with open(apikeyfile) as f:
        s = f.read()
    message = f"Your API Key is: {s}"
    choices = ["Looks Good!", "Change Stored API Key", "Exit"]
    output = easygui.buttonbox(message, title, choices)
    if output == "Looks Good!":
        asktype()
    elif output == "Change Stored API Key":
        ans = easygui.ynbox(msg = "Are you sure you want to remove your existing stored API Key?")
        if ans == True:            
            os.remove(apikeyfile)
            os.system("open https://platform.openai.com/account/api-keys")
            starthere()
        else:
            exit(0)
    else:
        exit(0)
            
            
def createkey(x):
    apikey = easygui.enterbox(x)
    return apikey


def getinfo(apikey, question):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apikey
    }

    data = {
        "model": getinfomodel,
        "prompt": question,
        "temperature": 0.9,
        "max_tokens": 3000,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.6,
        "stop": [" Human:", " AI:"]
    }
    
    response = requests.post(getinfourl, headers=headers, json=data)
    x = response.json()
    
    if response.status_code > 200:
        return(x['error']['message'])    
    else:
        return(x['choices'][0]['text'])


def getimage(apikey, question):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apikey
    }
    
    data = {
        "model": getimagemodel,
        "prompt": question,
        "n": 1,
        "size": "1024x1792"
        }    

    response = requests.post(getimageurl, headers=headers, json=data)
    x = response.json()    
    if response.status_code > 200:
        return(x['error']['message'])
    else:
        image_url = x['data'][0]['url']
        filename = f"{home}/Desktop/" + question.replace(" ","_") + ".png"
        img_data = requests.get(image_url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
            subprocess.call(['open', filename])                
        exit(1)


starthere()
