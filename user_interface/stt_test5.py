import speech_recognition as sr
a = sr.Recognizer()
with sr.Microphone() as source:
    print("say somthing")
    audio=a.listen(source)
    data=a.recognize_google(audio, language="ko")
    print(data)
