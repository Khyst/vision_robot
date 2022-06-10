import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import subprocess
import pyautogui

def speak(text):
    tts = gTTS(text=text, lang = "ko")
    filename="voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


room_list = ["화장실", "휴게실", "엘리베이터", "401호", "402호", "403호", "404호"]

if __name__ == "__main__":

    # 사용자가 원하는 위치 파일로 저장하기
    f = open("/home/cilab/ros_ws/src/cilab_nav/user_interface/output.txt", "w")

    while True:
        a = sr.Recognizer()
        with sr.Microphone() as source:
            print("say somthing")
            speak("명령을 말씀해주세요")
            audio=a.listen(source)
            data=a.recognize_google(audio, language = "ko")
            print(data)

            if(room_list[0] in data):
                speak("네 알겠습니다.")
                speak(room_list[0]+"로 안내하겠습니다.")
                f.write(room_list[0])
                break
                
            elif(room_list[1] in data):
                speak("네 알겠습니다.")
                speak(room_list[1]+"로 안내하겠습니다.")
                f.write(room_list[1])
                break

            elif(room_list[2] in data):
                speak("네 알겠습니다.")
                speak(room_list[2]+"로 안내하겠습니다.")
                f.write(room_list[2])
                break

            elif(room_list[3] in data):
                speak("네 알겠습니다.")
                speak(room_list[3]+"로 안내하겠습니다.")
                f.write(room_list[3])
                break

            elif(room_list[4] in data):
                speak("네 알겠습니다.")
                speak(room_list[4]+"로 안내하겠습니다.")
                f.write(room_list[4])
                break

            elif(room_list[5] in data):
                speak("네 알겠습니다.")
                speak(room_list[5]+"로 안내하겠습니다.")
                f.write(room_list[5])
                break
            elif("종료" in data):
                speak("네 알겠습니다.")
                speak("네 네비게이션을 종료합니다.")
                f.write("종료")

            else:
                speak("잘 모르겠습니다, 한번만 다시 말씀해주세요")

    f.close()