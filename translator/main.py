import speech_recognition as sr
import openai
import numpy as np
import pyaudio
import os
from pypinyin import pinyin, lazy_pinyin, Style
from gtts import gTTS
from flask import Flask, render_template, request
from playsound import playsound

chunk = 1024  # 記錄聲音的樣本區塊大小
# 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
sample_format = pyaudio.paInt16
channels = 2  # 聲道數量
# 取樣頻率，常見值為 44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025。
fs = 44100
seconds = 5  # 錄音秒數

app = Flask(__name__)

language_d = {"zh-tw": "中文", "en": "英文", "ja": "日文", "ko": "韓文"}
openai.api_key = "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"


@app.route("/")
def index():
    req = request.get_data()

    return render_template("index.html")


@app.route("/translate", methods=["GET"])
def openai_translate():
    language_word = request.values.get("langw", type=str)
    language_result = request.values.get("langre", type=str)

    lang_tr = language_d[language_word]
    lang_re = language_d[language_result]

    word = request.values.get("tword")

    messages = [
        {
            "role": "user",
            "content": f"扮演一台即時翻譯機，接下來我給你{lang_tr}就翻成{lang_re}，給你{lang_re}就翻譯成{lang_tr}，純粹翻譯就好，不要回答翻譯之外的文字",
        }
    ]

    messages.append({"role": "user", "content": word})  # 添加 user 回應

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", max_tokens=128, temperature=0.5, messages=messages
    )

    ai_msg = response.choices[0].message.content.replace("\n", "")

    messages.append({"role": "assistant", "content": ai_msg})  # 添加 ChatGPT 回應

    return render_template(
        "index.html",
        translate_word=word,
        translate_result=ai_msg,
        langwtxt=language_word,
        langretxt=language_result,
    )


@app.route("/listening", methods=["GET"])
def Mysecretary_listen():
    recognition = sr.Recognizer()
    with sr.Microphone() as source:
        # source 聲音的來源:電腦麥克風
        recognition.adjust_for_ambient_noise(source)
        audioData = recognition.listen(source)

    if audioData:
        # audioData 儲存聲源, language 指定語系
        content1 = recognition.recognize_google(audioData, language="zh-tw")
        # print(content1)

    else:
        content1 = ""

    return render_template("index.html", translate_word=content1)


@app.route("/play1", methods=["GET"])
def radio_play1():
    language_word = request.values.get("langw", type=str)
    language_result = request.values.get("langre", type=str)

    word = request.values.get("tword")
    result1 = request.values.get("tresult")

    tts_tr = gTTS(word, lang=language_word)
    tts_tr.save("static/word.mp3")
    playsound("static/word.mp3")
    os.remove("static/word.mp3")

    return render_template(
        "index.html",
        translate_word=word,
        translate_result=result1,
        langwtxt=language_word,
        langretxt=language_result,
    )


@app.route("/play2", methods=["GET"])
def radio_play2():
    language_word = request.values.get("langw", type=str)
    language_result = request.values.get("langre", type=str)

    word = request.values.get("tword")
    result1 = request.values.get("tresult")

    tts_re = gTTS(result1, lang=language_result)
    tts_re.save("static/word1.mp3")
    playsound("static/word1.mp3")
    os.remove("static/word1.mp3")

    return render_template(
        "index.html",
        translate_word=word,
        translate_result=result1,
        langwtxt=language_word,
        langretxt=language_result,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
