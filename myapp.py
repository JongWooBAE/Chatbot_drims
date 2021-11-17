from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from speech_recognition import *
from pyautogui import *
import clipboard
import keyboard
import pyaudio
import time # 필요한 모듈 불러오기
import wave
import sys
from gtts import gTTS
from playsound import playsound
import os
import os.path

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
#trainer.train("chatterbot.corpus.english")
#trainer.train("data/data.yml") #english
trainer.train("data/datako.yml") #korean

CHUNK = 1024

def audio():
    wf = wave.open("react.wav", 'rb')
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(CHUNK)
    
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
        
    stream.stop_stream()
    stream.close()

    p.terminate()
    
def read_voice(): # 음성 인식을 하는 함수
    r = Recognizer()
    mic = Microphone() # 마이크 객체
    
    with mic as source:
        audio = r.listen(source) # 음성 읽어오기
        
    voice_data = r.recognize_google(audio, language='ko')
    return voice_data # 값 반환

@app.route("/")
def index():
	return render_template("index.html")     #to send context to html

@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg")      #get data from input, we write js to index.html
    return str(english_bot.get_response(userText))

@app.route("/record/user")
def start_record():
    print('record')
    audio()     #지정된 호출을 출력
    print("입력2")
    h = str(os.getcwd().replace("\\", "/")+"/sample.mp3")
    try:        
        voice = read_voice() # 음성 인식
        answer = str(english_bot.get_response(voice))
        print(voice+":"+answer)
        time.sleep(0.1) 
        if os.path.isfile(h):
            os.remove(h)
        print(h)
        s = gTTS(answer, lang="ko")
        s.save(h)
        playsound(h)
        time.sleep(1)
        return voice+":"+answer
    except:
        if os.path.isfile(h):
            os.remove(h)
        s = gTTS("오류가 발생했어요.", lang="ko")
        s.save(h)
        playsound(h)
        time.sleep(1)
        os.remove(h)
        

if __name__ == "__main__":
	app.run(debug = True)