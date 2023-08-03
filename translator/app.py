import speech_recognition as sr
import openai
import pyttsx3
from tqdm import tqdm
import threading
import numpy as np
import pyaudio
import pyaudio
from pypinyin import pinyin, lazy_pinyin, Style

import flask

app = flask.Flask(__name__)


@app.route("/")
@app.route("/app")
def hello():
    return "Hello, World!"


@app.route("/app123")
def hello1():
    return "Hello, World!123"


def play_audio(wave_input_path):
    global action
    p = pyaudio.PyAudio()
    wf = wave.open(wave_input_path, "rb")
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )


def Mysecretary_listen():
    recoginition = sr.Recognizer()
    with sr.Microphone() as source:
        # source 聲音的來源:電腦麥克風
        print("說話")
        audioData = recoginition.listen(source, 5, 5)
        print(2)

    try:
        # audioData 儲存聲源, language 指定語系
        print("錄音結束..")
        content1 = recoginition.recognize_google(audioData, language="zh-tw")
        print(content1)
        # content2 = lazy_pinyin(content1)
        # print(content2)
        return content1

    except:
        return "請再說一遍!!"


messages = []


def openaiGPT_voice(msg):
    openai.api_key = "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"

    messages.append({"role": "user", "content": msg})  # 添加 user 回應
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", max_tokens=335, temperature=0.5, messages=messages
    )
    ai_msg = response.choices[0].message.content.replace("\n", "")
    messages.append({"role": "assistant", "content": ai_msg})  # 添加 ChatGPT 回應
    print(f"ChatGPT: {ai_msg}")

    # print(messages)
    # 語音播放
    eng = pyttsx3.init()
    eng.say(ai_msg)
    eng.runAndWait()


def openaiGPT_txt(msg):
    openai.api_key = "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"

    messages.append({"role": "user", "content": msg})  # 添加 user 回應
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", max_tokens=335, temperature=0.5, messages=messages
    )
    ai_msg = response.choices[0].message.content.replace("\n", "")
    messages.append({"role": "assistant", "content": ai_msg})  # 添加 ChatGPT 回應
    print(f"ChatGPT: {ai_msg}")

    # print(messages)
    # 語音播放
    eng = pyttsx3.init()
    eng.say(ai_msg)
    eng.runAndWait()


if __name__ == "__main__":
    question = Mysecretary_listen()
    sentence = ""
    for i in question:
        sentence += str(i)

    app.run("0.0.0.0", debug=True)
