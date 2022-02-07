#Developed by 
'''SQUARDRON!'''
import os
import time
import requests
import cv2
import warnings
from playsound import playsound
from datetime import date
from datetime import datetime
from tkinter import *
from win10toast import ToastNotifier
from win32api import GetSystemMetrics
import speech_recognition as sr
import mysql.connector
from PIL import ImageTk
import PIL.Image as pl 
import piglet

#Connecting to MySQL Server
clinicon_sql_server = mysql.connector.connect(
  host="localhost",
  user="root",
  password="lenovog500s",
  database="clinicon"
)
sql_cursor = clinicon_sql_server.cursor()

#Detecting Microphone
mic_name = "Microphone Array (Realtek High "
sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer() 
mic_list = sr.Microphone.list_microphone_names()
for i, microphone_name in enumerate(mic_list): 
	if microphone_name == mic_name: 
		device_id = i

#Speech to Text
def cliniconGetData(return_statement):
        with sr.Microphone(device_index = device_id, sample_rate = sample_rate, 
						chunk_size = chunk_size) as source: 
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source) 
		
            try: 
                    text = r.recognize_google(audio)
                    if(return_statement=="gender"):
                        if(text[0]=="M" or text[0]=="m" ):
                            text="Male"
                    return_statement=text
                    return(text.capitalize())
	
            except sr.UnknownValueError: 
                    return("audio_error")
	
            except sr.RequestError as e: 
                    return("request_error")


#preprocessed data
screen_width = GetSystemMetrics(0) #864
screen_height = GetSystemMetrics(1) #1536
icon_path=os.path.join(os.path.dirname(__file__),"pictures/icon.ico")
home_intro_path=os.path.join(os.path.dirname(__file__),"audio/home.mp3")
today = date.today()
now = datetime.now()
warnings.filterwarnings("ignore")

#live time updation
def updateTime():
    now = datetime.now()
    current_time=now.strftime("%H:%M:%S")
    lab5["text"]=str(current_time)+"\n"
    root.after(200,updateTime)

#Get Internet Connection
def getInternetStatus():
    try:
        r = requests.get("https://www.google.com/",timeout=3)
    except requests.exceptions.HTTPError as errh:
        in_connection=0
    except requests.exceptions.ConnectionError as errc:
        in_connection=0
    except requests.exceptions.Timeout as errt:
        in_connection=0
    except requests.exceptions.RequestException as err:
        in_connection=0
    else:
        in_connection=1
    
    if(in_connection==1):
        net2["text"]="Connected,Secure\n"
        net_image["image"]=tick
    else:
        net2["text"]="No Internet Access\n"
        net_image["image"]=cross
    root.after(2000,getInternetStatus)

#disable numpad
def disableNumpad(childList):
    for child in childList:
        child.configure(state='disable')

#enable numpad
def enableNumpad(childList):
    for child in childList:
        child.configure(state='normal')

def detectFace():
    face_features=os.path.join(os.path.dirname(__file__),"haarcascade_frontalface_default.xml")
    video=cv2.VideoCapture(0)
    cas_classify=cv2.CascadeClassifier(face_features)
    s1=0
    flag=0
    gen_start=time.time()
    while True:
        check,frame=video.read()
        gray_image=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        detect_face=cas_classify.detectMultiScale(gray_image,1.1,3 )
        
        for x,y,w,h in detect_face:
            cv2.rectangle(frame, (x,y),(x+w,y+h),(129, 200 , 71), 3)
        
        cv2.imshow("CLINICON - Detecting Face", frame)
        cv2.waitKey(1)
        if detect_face!=() and flag==0:
            s1=time.time()
            flag=1
        if(abs(s1-time.time())>=2.5)and flag==1:
            dett=1
            break
        if(abs(gen_start-time.time())>=11):
            dett=0
            break
    video.release()
    cv2.destroyAllWindows()
    if(dett==1):
        return 1
    else:
        return 0

def thermalSimulation():
    face_features=os.path.join(os.path.dirname(__file__),"haarcascade_frontalface_default.xml")
    video=cv2.VideoCapture(0)
    cas_classify=cv2.CascadeClassifier(face_features)
    s1=0
    flag=0
    while True:
        check,frame=video.read()
        gray_image=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        detect_face=cas_classify.detectMultiScale(gray_image,1.1,3 )
        
        clinicon_thermal_map = cv2.applyColorMap(frame, cv2.COLORMAP_HSV)
        cv2.imshow("CLINICON - Thermal Simulation(Output)", clinicon_thermal_map)
        cv2.waitKey(1)
        if detect_face!=() and flag==0:
            s1=time.time()
            flag=1
        if(abs(s1-time.time())>=4.5)and flag==1:
            break
    video.release()
    cv2.destroyAllWindows()

#some useful var
global pat_Name
pat_Name = ""
global pat_Gender
pat_Gender = ""
global pat_Age
pat_Age = ""
global pat_Aadhar
pat_Aadhar = ""
global pat_Contact
pat_Contact = ""
global pat_Weight
pat_Weight = ""
global pat_Height
pat_Height = ""
#keyword Counter
global prime
prime=[]
global sec
sec=[]

def setOne6(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(6)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=None
    red_but["command"]=None
    c1,c2=0,0
    for i in sec:
        if(i in [1,3,5]):
            c1+=1
        else:
            c2+=1
    if(c1==c2):
        Label(text_space ,text="You have both symptoms of Malaria and Typhoid" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        #Label(text_space ,text="\n" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Malaria) = P(Typhoid) = 0.5" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    elif(c2>c1):
        prob=(c2/3)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Typhoid" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Typhoid)="+str("%0.2f" %prob)+"\n" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    else:
        prob=(c1/3)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Malaria" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Malaria)="+str("%0.2f" %prob)+"\n" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    Label(text_space ,text="YOU HAVE SYMPTOMS OF SERIOUS DISEASE\nPLEASE GO TO THE NEARBY PUBLIC HEALTH CARE CENTER." ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="THE REPORT IS SENT TO THE MEDICAL FACILITY FOR IMMEDIATE ATTENTION" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne5(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(5)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne6(1)
    red_but["command"]=lambda:setOne6(0)
    Label(text_space ,text="Do you have rose spots in abdomen?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/abdomen.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne4(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(4)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne5(1)
    red_but["command"]=lambda:setOne5(0)
    Label(text_space ,text="Do you suffer from abdominal and body pain?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/abdominalbody.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne3(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(3)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne4(1)
    red_but["command"]=lambda:setOne4(0)
    Label(text_space ,text="Do you lose your appetite?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/appetite.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne2(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(2)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne3(1)
    red_but["command"]=lambda:setOne3(0)
    Label(text_space ,text="Do you suffer from Night Sweats?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/nightsweats.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne1(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(1)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne2(1)
    red_but["command"]=lambda:setOne2(0)
    Label(text_space ,text="Did your body temperature increase gradually?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/bodytempinc.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo6(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(8)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=None
    red_but["command"]=None
    c1,c2=0,0
    for i in sec:
        if(i in [1,3,4,6]):
            c1+=1
        else:
            c2+=1
    if(c1>c2):
        prob=(c1/4)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Tuberculosis" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Tuberculosis)="+str("%0.2f" %prob)+"\n" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="YOU HAVE SYMPTOMS OF SERIOUS DISEASE\nPLEASE GO TO THE NEARBY PUBLIC HEALTH CARE CENTER." ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    else:
        prob=(c2/4)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Common Cold" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Common Cold)="+str("%0.2f" %prob) ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    
    Label(text_space ,text="THE REPORT IS SENT TO THE MEDICAL FACILITY FOR IMMEDIATE ATTENTION" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo5(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(6)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo6(1)
    red_but["command"]=lambda:setTwo6(0)
    Label(text_space ,text="Do you suffer from running nose?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo4(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(5)
        sec.append(7)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo5(1)
    red_but["command"]=lambda:setTwo5(0)
    Label(text_space ,text="Did you have sudden weight loss?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo3(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(3)
        sec.append(4)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo4(1)
    red_but["command"]=lambda:setTwo4(0)
    Label(text_space ,text="Did you suffer from Mild or High Fever?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo2(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(2)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo3(1)
    red_but["command"]=lambda:setTwo3(0)
    Label(text_space ,text="Do you have Chest pain and rise in temperature during evenings and nights?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo1(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(1)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo2(1)
    red_but["command"]=lambda:setTwo2(0)
    Label(text_space ,text="Do you suffer from Nasal Congestion?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/nasal.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree6(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(6)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=None
    red_but["command"]=None
    c1,c2=0,0
    for i in sec:
        if(i in [1,3,5]):
            c1+=1
        else:
            c2+=1
    if(c1==c2):
        Label(text_space ,text="You have both symptoms of Gastric Ulcer and Worm Infestation" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        #Label(text_space ,text="\n" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Gastric Ulcer) = P(Worm Infestation) = 0.5" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    elif(c2>c1):
        prob=(c2/3)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Worm Infestation" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Worm Infestation)="+str("%0.2f" %prob)+"\n" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    else:
        prob=(c1/3)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Gastric Ulcer" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Gastric Ulcer)="+str("%0.2f" %prob)+"\n" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    Label(text_space ,text="YOU HAVE SYMPTOMS OF SERIOUS DISEASE\nPLEASE GO TO THE NEARBY PUBLIC HEALTH CARE CENTER." ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="THE REPORT IS SENT TO THE MEDICAL FACILITY FOR IMMEDIATE ATTENTION" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree5(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(5)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree6(1)
    red_but["command"]=lambda:setThree6(0)
    Label(text_space ,text="Do you suffer from Muscle Cramp?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree4(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(4)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree5(1)
    red_but["command"]=lambda:setThree5(0)
    Label(text_space ,text="Do you have severe Abdominal Pain?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree3(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(3)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree4(1)
    red_but["command"]=lambda:setThree4(0)
    Label(text_space ,text="Did you suffer from Itchiness around the anus?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree2(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(2)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree3(1)
    red_but["command"]=lambda:setThree3(0)
    Label(text_space ,text="Do you suffer from Nausea?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree1(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(1)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree2(1)
    red_but["command"]=lambda:setThree2(0)
    Label(text_space ,text="Do you suffer from Blood from stool?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour7(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(7)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=None
    red_but["command"]=None
    c1,c2=0,0
    for i in sec:
        if(i in [2,4,5,7]):
            if(i==2):
                c2+=1
            c1+=1
        else:
            c2+=1
    if(c1>=c2):
        prob=(c1/4)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Anaemia" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Anaemia)="+str("%0.2f" %prob)+"\n" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="YOU HAVE SYMPTOMS OF SERIOUS DISEASE\nPLEASE GO TO THE NEARBY PUBLIC HEALTH CARE CENTER." ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    else:
        prob=(c2/4)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Dehydration" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Dehydration)="+str("%0.2f" %prob) ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    
    Label(text_space ,text="THE REPORT IS SENT TO THE MEDICAL FACILITY FOR IMMEDIATE ATTENTION" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour6(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(6)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour7(1)
    red_but["command"]=lambda:setFour7(0)
    Label(text_space ,text="Do you feel like Fainting?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour5(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(5)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour6(1)
    red_but["command"]=lambda:setFour6(0)
    Label(text_space ,text="Do you suffer from confusion?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour4(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(4)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour5(1)
    red_but["command"]=lambda:setFour5(0)
    Label(text_space ,text="Do you suffer from Breathlessness?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour3(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(3)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour4(1)
    red_but["command"]=lambda:setFour4(0)
    Label(text_space ,text="Does your pulse rate is higher than usual?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour2(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(2)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour3(1)
    red_but["command"]=lambda:setFour3(0)
    Label(text_space ,text="Does your urine looks dark?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour1(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(1)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour2(1)
    red_but["command"]=lambda:setFour2(0)
    Label(text_space ,text="Do you feel Tired?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def startSecondary(n):
    if((2 in prime) and (3 in prime) and(4 in prime)):
        Label(text_space ,text="1. High Fever with shivering?\n2. Gradual increase in temperature throught the day?\n3. Night sweats?\n4. Loss of appetite?\n5. Abdominal / Body pain?\n6. Rose spots in abdomen?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        Label(text_space ,text="Do you have high fever with shivering?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        green_but["command"]=lambda:setOne1(1)
        red_but["command"]=lambda:setOne1(0)
    elif((1 in prime) and (2 in prime)):
        Label(text_space ,text="1. Cough with increased sputum or blood?\n2. Nasal congestion?\n3. Chest pain and rise in temperature during evenings and nights?\n4. Mild fever?\n5. Sudden weight loss?\n6. Runny nose?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        Label(text_space ,text="Do you have cough with increased sputum or blood?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        green_but["command"]=lambda:setTwo1(1)
        red_but["command"]=lambda:setTwo1(0)
    elif((3 in prime) and (4 in prime)):
        Label(text_space ,text="1. Heart burn (or) Regurgitation?\n2. Blood in stool?\n3. Nausea?\n4. Itchiness around the anus?\n5. Severe Abdominal pain?\n6. Muscle cramp?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        playsound(os.path.join(os.path.dirname(__file__),"audio/heartburn.mp3"))
        Label(text_space ,text="Do you suffer from Heart burn or Regurgitation?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        green_but["command"]=lambda:setThree1(1)
        red_but["command"]=lambda:setThree1(0)
    elif((5 in prime) and (6 in prime)):
        Label(text_space ,text="1. Extreme thirst?\n2. Tiredness?\n3. Dark coloured urine?\n4. Fast heart rate?\n5. Breathlessness?\n6. Confusion?\n7. Fainting episodes?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")

        Label(text_space ,text="Do you suffer from Extreme Thirst?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        green_but["command"]=lambda:setFour1(1)
        red_but["command"]=lambda:setFour1(0)
    else:
        Label(text_space ,text="Hey!! "+pat_Name +"\nYou just have common infection...\nYou will be alright...Eat healthy and take some rest\nTake the medicine mentioned in Medicine tab",bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
    

def getHead(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(6)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:startSecondary(1)
    red_but["command"]=lambda:startSecondary(0)
    Label(text_space ,text="Analysing...\nPreparing Secondary set of Symptoms!" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/secondarysymp.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    startSecondary(1)

def getDizzy(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(5)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getHead(1)
    red_but["command"]=lambda:getHead(0)
    Label(text_space ,text="Do you suffer from Headache?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/headache.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def getVomit(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(4)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getDizzy(1)
    red_but["command"]=lambda:getDizzy(0)
    Label(text_space ,text="Do you suffer from Dizziness?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/dizziness.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def getAbpain(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(3)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getVomit(1)
    red_but["command"]=lambda:getVomit(0)
    Label(text_space ,text="Did you Vomit?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def getFever(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(2)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getAbpain(1)
    red_but["command"]=lambda:getAbpain(0)
    Label(text_space ,text="Do you have Abdominal or Stomach Pain?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/abdomenstomach.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def getCough(n):
    if(n==1):
        Label(text_space ,text="Yes" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(1)
    else:
        Label(text_space ,text="No" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getFever(1)
    red_but["command"]=lambda:getFever(0)
    Label(text_space ,text="Do you have Fever?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/fever.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")



def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def getSymptoms():
    try:
        frame2.place_forget()
    except NameError:
        pass
    try:
        dia_frame.place_forget()
    except NameError:
        pass
    try:
        number_pad.place_forget()
    except NameError:
        pass
    global chat_bot
    chat_bot = LabelFrame(root,bg="#222831",relief=GROOVE,borderwidth=0)
    chat_bot.place(x=500,y=127,height=617,width=580)
    global text_area
    text_area=Canvas(chat_bot,bg="#78Bfff",relief=GROOVE)
    text_area.place(x=7,y=5,height=450,width=564)
    global text_space
    text_space=Frame(text_area,bg="#78Bfff",relief=GROOVE)
    #text_space.place(x=7,y=5,height=437,width=547)
    
    global scroll
    scroll = Scrollbar(text_area, orient="vertical", command=text_area.yview)
    text_area.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    text_area.create_window((20,20), window=text_space,width=540)
    text_space.bind("<Configure>", lambda event, canvas=text_area: onFrameConfigure(canvas))

    global green_but
    green_but=Button(chat_bot,bg="#cff09e",image=green,bd=0,padx=35,pady=30,command=lambda:getCough(1))
    green_but.place(x=90,y=470)
    global red_but
    red_but=Button(chat_bot,bg="#f4b2b0",image=red,bd=0,padx=35,pady=30,command=lambda:getCough(0))
    red_but.place(x=350,y=470)

    playsound(os.path.join(os.path.dirname(__file__),"audio/cliniconwelcome.mp3")) # 1.Hi I'm baju an inbuilt assistant 2. Press the button to respond
    Label(text_space ,text="Hi, You're visiting Clinicon. You are safe now. Let us get you diagnosed!" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    #time.sleep(2)
    Label(text_space ,text="Let's start the diagnosing procedure" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/procedure.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    #time.sleep(2)
    Label(text_space ,text="Select your primary Symptoms" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/primarysymp.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    #time.sleep(2)
    Label(text_space ,text="Do you have cough?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"audio/cough.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")

def getTemp():
    dia_title["text"]="Getting Temperature"
    dia_image["image"]=step10
    playsound(os.path.join(os.path.dirname(__file__),"audio/temp.mp3")) #Thermal Simulation
    time.sleep(2)
    thermalSimulation()
    dia_result["text"]="Simulated-ex: Temp - 97.5°C"
    namebut["command"]=getSymptoms

def getPhoto():
    global pat_Weight
    if(pat_Weight=="" or int(pat_Weight)<20 or int(pat_Weight)>147):
        pat_Weight = dia_result["text"]
    if(int(pat_Weight)<20 or int(pat_Weight)>147):
        noti = ToastNotifier()
        noti.show_toast("CLINICON","Invalid Weight, Please enter Weight in kg",icon_path=icon_path,duration=3)
        getWeight()
        return
    dia_title["text"]="Capturing Photo"
    dia_image["image"]=step9
    #area to update db -- Weight
    playsound(os.path.join(os.path.dirname(__file__),"audio/placeyourface.mp3")) #detecting face
    d_face=detectFace()
    if(d_face==1):
        dia_result["text"]="Face Detected"
        playsound(os.path.join(os.path.dirname(__file__),"audio/photocaptured.mp3")) #Face detected capturing Photo
    else:
        dia_result["text"]="Can't Detect Face...Starting Again"
        playsound(os.path.join(os.path.dirname(__file__),"audio/phototimeelapsed.mp3")) #Face Time Elapsed Trying Again
        getPhoto()
    #capture photo and save it
    #fswebcam and open the pic for 3 seconds
    dia_result["text"]="Photo Captured"
    namebut["command"]=getTemp

def getWeight():
    global pat_Height
    if(pat_Height=="" or int(pat_Height)<110 or int(pat_Height)>205):
        pat_Height = dia_result["text"]
    if(int(pat_Height)<110 or int(pat_Height)>205):
        noti = ToastNotifier()
        noti.show_toast("CLINICON","Invalid Height, Please enter height in cm",icon_path=icon_path,duration=3)
        getHeight()
        return
    dia_title["text"]="Enter Your Weight (in Kg)"
    dia_image["image"]=step8
    #area to update db -- Height
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"audio/weight.mp3"))

    namebut["command"]=getPhoto



def getHeight():
    global pat_Contact
    if(pat_Contact=="" or len(pat_Contact)!=10):
        pat_Contact = dia_result["text"]

    if(len(pat_Contact)!=10):
        noti = ToastNotifier()
        noti.show_toast("CLINICON","Invalid Contact No",icon_path=icon_path,duration=3)
        getContact()
        return
    dia_title["text"]="Enter Your Height (in cm)"
    dia_image["image"]=step7
    #area to update db -- Contact
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"audio/height.mp3"))

    namebut["command"]=getWeight

def getContact():
    global pat_Aadhar
    if(pat_Aadhar=="" or len(pat_Aadhar)!=12):
        pat_Aadhar = dia_result["text"]

    if(len(pat_Aadhar)!=12):
        noti = ToastNotifier()
        noti.show_toast("CLINICON","Invalid Aadhar No",icon_path=icon_path,duration=3)
        getAadhar()
        return
    dia_title["text"]="Enter Your Contact no"
    dia_image["image"]=step6
    #area to update db -- Aadhar
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"audio/contact.mp3"))

    namebut["command"]=getHeight

def getAadhar():
    global pat_Age
    if(pat_Age=="" or int(pat_Age)<7 or int(pat_Age)>95):
        pat_Age = dia_result["text"]
    print(pat_Age)
    if(int(pat_Age)<7 or int(pat_Age)>95):
        noti = ToastNotifier()
        noti.show_toast("CLINICON","Age is not permitted or Invalid Age",icon_path=icon_path,duration=3)
        getAge()
        return
    dia_title["text"]="Enter Your Aadhar"
    dia_image["image"]=step5
    #area to update db -- Age
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"audio/aadhar.mp3"))

    namebut["command"]=getContact

def getAge():
    dia_title["text"]="Enter Your Age"
    dia_image["image"]=step4
    girl_but.place_forget()
    boy_but.place_forget()
    enableNumpad(number_pad.winfo_children())
    #area to update db -- gender
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"audio/age.mp3"))

    namebut["command"]=getAadhar

def enter(n):
    dia_result["text"]=dia_result["text"]+str(n)

def clear_value():
    dia_result["text"]=""

def setGender(gender):
    namebut.place(x=617,y=5)
    global pat_Gender
    pat_Gender = gender
    #namebut["command"]=getAge
    #voice **gender** selected
    patient_gender=gender
    getAge()

def getGender():
    dia_title["text"]="Recite Your Gender"
    dia_image["image"]=step3
    namebut.place_forget()
    retry_button.place_forget()
    #area to update db -- name
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"audio/gender.mp3"))
    #name=cliniconGetData("gender")
    #dia_result["text"]=name
    global girl_but
    girl_but = Button(dia_frame,bg="#FFDBE9",image=girl,bd=0,padx=35,pady=30,command=lambda:setGender("Female"))
    girl_but.place(x=400,y=567)
    global boy_but
    boy_but = Button(dia_frame,bg="#8FD3FE",image=boy,bd=0,padx=35,pady=30,command=lambda:setGender("Male"))
    boy_but.place(x=137,y=567)
    retry_button["command"]=getGender


def getName():
    dia_title["text"]="Recite Your Name"
    dia_image["image"]=step2
    playsound(os.path.join(os.path.dirname(__file__),"audio/name.mp3"))
    name=cliniconGetData("name")
    dia_result["text"]=name
    global pat_Name
    pat_Name=name
    wel1["text"]=(name+"\n")
    namebut["command"]=getGender
    retry_button.place(x=10,y=5)
    retry_button["command"]=getName
    if(name=="audio_error"):
        dia_result["text"]="Can't Recognize, Listening Again"
        getName()
        return

    

def generateID():
    dia_title["text"]="Note your ID"
    dia_image["image"]=step1
    playsound(os.path.join(os.path.dirname(__file__),"audio/id.mp3"))
    #logic to generate ID

    dia_result["text"]="CSIH077" #change with variable
    lab10["text"]="ID"
    lab11["text"]="CSIH077" #change with variable
    namebut["command"]=getName
    retry_button.place_forget()
    disableNumpad(number_pad.winfo_children())


def startDiagnosing():
    global dia_frame
    dia_frame = LabelFrame(root,bg="#fbd46d",relief=GROOVE)
    frame2.place_forget()
    dia_frame.place(x=277,y=107,height=707,width=657)
    global dia_title
    dia_title=Label(dia_frame,text="",bg="#222831",fg="#ddf3f5",font=("Ubuntu",32),anchor=CENTER)
    dia_title.pack()
    global dia_image
    dia_image=Label(dia_frame,bg="#222831")
    dia_image.pack()
    global dia_result
    dia_result=Label(dia_frame,text="----------",bg="#222831",fg="#ffffff",font=("Ubuntu",30))
    dia_result.pack()
    global namebut
    namebut=Button(dia_frame,padx=5,pady=5,image=next_img)
    namebut.place(x=617,y=5)
    global retry_button
    retry_button=Button(dia_frame,image=rety,padx=5,pady=5)
    retry_button.place(x=10,y=5)

    global number_pad
    number_pad = LabelFrame(root,bg="#222831",relief=GROOVE)
    number_pad.place(x=967,y=107,height=527,width=370)
    b1=Button(number_pad,text="1",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("1"),bd=0,padx=35,pady=30)
    b2=Button(number_pad,text="2",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("2"),bd=0,padx=35,pady=30)
    b3=Button(number_pad,text="3",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("3"),bd=0,padx=35,pady=30)
    b4=Button(number_pad,text="4",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("4"),bd=0,padx=35,pady=30)
    b5=Button(number_pad,text="5",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("5"),bd=0,padx=35,pady=30)
    b6=Button(number_pad,text="6",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("6"),bd=0,padx=35,pady=30)
    b7=Button(number_pad,text="7",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("7"),bd=0,padx=35,pady=30)
    b8=Button(number_pad,text="8",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("8"),bd=0,padx=35,pady=30)
    b9=Button(number_pad,text="9",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("9"),bd=0,padx=35,pady=30)
    b0=Button(number_pad,text="0",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("0"),bd=0,padx=35,pady=30)
    bdot=Button(number_pad,text=".",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:enter("."),bd=0,padx=35,pady=30)
    bclear=Button(number_pad,text="CLR",fg="#ffffff",bg="#c41212",font=('Ubuntu',22,"bold"),bd=0,padx=30,pady=32,command=clear_value)

    b1.grid(row=1,column=0,sticky=W+E+N+S)
    b2.grid(row=1,column=1,sticky=W+E+N+S)
    b3.grid(row=1,column=2,sticky=W+E+N+S)
    b4.grid(row=2,column=0,sticky=W+E+N+S)
    b5.grid(row=2,column=1,sticky=W+E+N+S)
    b6.grid(row=2,column=2,sticky=W+E+N+S)
    b7.grid(row=3,column=0,sticky=W+E+N+S)
    b8.grid(row=3,column=1,sticky=W+E+N+S)
    b9.grid(row=3,column=2,sticky=W+E+N+S)
    b0.grid(row=4,column=1,sticky=W+E+N+S)
    bdot.grid(row=4,column=2,sticky=W+E+N+S)
    bclear.grid(row=4,column=0,sticky=W+E+N+S)
    generateID()

#contains menu
def nameFrame():
    global frame2
    frame2 = LabelFrame(root,bg="#222831",relief=GROOVE)
    frame2.place(x=500,y=147,height=550,width=700)
    l1=Button(frame2,text="Start Diagnosing",bg="#f6006b",fg="#dae1e7",font=("Ubuntu",17),padx=20,pady=20,width=20,command=startDiagnosing)

    #frame1.place_forget()
    l1.place(x=200,y=200)
    


def welcomeFrame():
    global frame1
    frame1 = Frame(root,bg="#222831",relief=GROOVE)
    frame1.place(x=45,y=107,height=667,width=317)
    lab1=Label(frame1,text="Welcome!",bg="#222831",fg="#01b4f5",font=("Ubuntu",16),anchor=W)
    lab1.grid(row=0,column=0,sticky=W+E)
    global wel1
    wel1=Label(frame1,text="\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    wel1.grid(row=1,column=0,sticky=W+E)
    lab2=Label(frame1,text="Date",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab2.grid(row=2,column=0,sticky=W+E)
    lab3=Label(frame1,text=today.strftime("%B %d, %Y")+"\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab3.grid(row=3,column=0,sticky=W+E)
    lab4=Label(frame1,text="Local Time",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab4.grid(row=4,column=0,sticky=W+E)
    global lab5
    lab5=Label(frame1,text=now.strftime("%H:%M:%S")+"\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab5.grid(row=5,column=0,sticky=W+E)
    lab6=Label(frame1,text="Device ID",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab6.grid(row=6,column=0,sticky=W+E)
    lab7=Label(frame1,text="CLINI07AH\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab7.grid(row=7,column=0,sticky=W+E)
    lab8=Label(frame1,text="Location",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab8.grid(row=8,column=0,sticky=W+E)
    lab9=Label(frame1,text="Kuruvadipatti\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab9.grid(row=9,column=0,sticky=W+E)
    global net_image
    global net2
    net1=Label(frame1,text="Internet",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    net1.grid(row=10,column=0,sticky=W+E)
    net2=Label(frame1,text="\n",bg="#222831",fg="#ffffff",font=("Ubuntu",14),anchor=W,padx=0)
    net2.grid(row=11,column=0,padx=0,sticky=W+E+S+N)
    net_image=Label(frame1,bg="#222831",padx=0,anchor=N)
    net_image.grid(row=11,column=1,padx=0,sticky=W+E+S+N)
    global lab10
    global lab11
    lab10=Label(frame1,text="\n",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab10.grid(row=12,column=0,sticky=W+E)
    lab11=Label(frame1,text="\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab11.grid(row=13,column=0,sticky=W+E)
    

def goToHome():
    try:
        chat_bot.place_forget()
    except NameError:
        pass
    try:
        dia_frame.place_forget()
    except NameError:
        pass
    try:
        number_pad.place_forget()
    except NameError:
        pass
    frame2.place(x=500,y=147,height=550,width=700)

if __name__ == "__main__":
    root=Tk()
    root.title("CLINICON - Medical Assistant(Beta)")
    root.iconbitmap(icon_path)
    root.state('zoomed')
    root.configure(bg="#222831")
    #root.attributes('-fullscreen', True)
    root.geometry(str(screen_width)+"x"+str(screen_height))

    constant_label=Label(root,text="CLINICON",bg="#222831",fg="#ffffff",font=("Ubuntu",34,"bold"))
    constant_label.place(x=27,y=27)
    #required images
    home_button_image=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/homebut.png")))
    step1=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/1.png")))
    step2=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/2.png")))
    step3=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/3.png")))
    step4=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/4.png")))
    step5=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/5.png")))
    step6=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/6.png")))
    step7=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/7.png")))
    step8=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/8.png")))
    step9=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/9.png")))
    step10=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/10.png")))
    next_img=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/next.png")))
    tick=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/tick.png")))
    cross=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/cross.png")))
    rety=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/rety.png")))
    green=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/green.png")))
    red=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/red.png")))
    #check=pl.open(os.path.join(os.path.dirname(__file__),"name.gif"))
    girl=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/girl.png")))
    boy=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/boy.png")))


    home_button=Button(root,text="Home",bg="#ffffff",fg="#ffffff",font=("Ubuntu",5,"bold"),image=home_button_image,height=24,width=24,command=goToHome)
    home_button.place(x=1477,y=27)
    
    welcomeFrame()
    nameFrame()

    updateTime() #calling update time fn
    getInternetStatus() #Internet Status
    
    root.mainloop()

