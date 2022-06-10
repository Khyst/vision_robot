import os
 
def speak(option, msg) :
    os.system("espeak {} '{}'".format(option,msg))
    
option = '-s 160 -p 95 -a 200 -v ko+f3'
msg = '안녕하세요 반가워요'
 
print('espeak', option, msg)
speak(option,msg)