import speech_recognition as sr
from gtts import gTTS
import playsound

def speak(text):
    tts = gTTS(text=text, lang = "ko")
    filename="voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)




a = sr.Recognizer()
with sr.Microphone() as source:
    print("say somthing")
    audio=a.listen(source)
    data=a.recognize_google(audio)
    print(data)

    if(data == "안녕하세요"):
        speak("안녕하세요")
    else:
        speak("잘모르겠습니다.")


