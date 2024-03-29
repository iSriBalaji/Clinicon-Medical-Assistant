#Developed by 
'''Sri Balaji Muruganandam & Abhishek Pughazhendhi'''
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
#sql_cursor = clinicon_sql_server.cursor()

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
doc_upload_path=os.path.join(os.path.dirname(__file__),"document.png")
patient_photo=os.path.join(os.path.dirname(__file__),"patient.png")
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
            cv2.imwrite(patient_photo,frame)
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
global covid19
covid19=[]

def scanDocument():
    video=cv2.VideoCapture(0)
    gen_start=time.time()
    while True:
        check,frame=video.read()
        cv2.imshow("CLINICON - Upload Document", frame)
        cv2.waitKey(1)

        if(abs(gen_start-time.time())>=5):
            cv2.imwrite(doc_upload_path,frame)
            break
    video.release()
    cv2.destroyAllWindows()
    doc_result["text"] = "दस्तावेज़ अपलोड किया गया" #Document Uploaded   
def addDocuments():
    try:
        frame2.place_forget()
    except NameError:
        pass
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
    try:
        covid_frame.place_forget()
    except NameError:
        pass
    try:
        data_frame.place_forget()
    except NameError:
        pass
    global doc_frame
    doc_frame = LabelFrame(root,bg="#222831",relief=GROOVE)
    doc_frame.place(x=487,y=107,height=707,width=657)
    global doc_title
    doc_title=Label(doc_frame,text="अपने दस्तावेज़ अपलोड करें",bg="#222831",fg="#ddf3f5",font=("Ubuntu",32),anchor=CENTER) #Upload your Documents
    doc_title.pack()
    global doc_image
    doc_image=Label(doc_frame,bg="#222831",image=upload_doc_image)
    doc_image.pack()
    global doc_result
    doc_result=Label(doc_frame,text="",bg="#222831",fg="#ffffff",font=("Ubuntu",30))
    doc_result.pack()
    global doc_finish
    doc_finish=Button(doc_frame,padx=5,pady=5,text="समाप्त", font=('Ubuntu',11,"bold"),command=goToHome)
    doc_finish.place(x=583,y=5)
    global plus_button
    plus_button=Button(doc_frame,image=plus,padx=5,pady=5,command=scanDocument)
    plus_button.place(x=10,y=5)

def setOne6(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(6)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
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
        Label(text_space ,text="आपको मलेरिया और टाइफाइड दोनों लक्षण हैं" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/malariatyphoid.mp3"))
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
    Label(text_space ,text="आप गंभीर छूट के लक्षण हैं\nकृपया सार्वजनिक स्वास्थ्य देखभाल केंद्र के पास जाएं." ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/seriousdisease.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="रिपोर्ट को ध्यान केंद्रित करने के लिए चिकित्सा सुविधा के लिए भेजा गया है" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    green_but.place_forget()
    red_but.place_forget()
    final_but = Button(chat_bot,text="दस्तावेज़ अपलोड करें",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=addDocuments,bd=0,padx=12,pady=10)
    final_but.place(x=110,y=470)
    fi_but = Button(chat_bot,text="समाप्त",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=goToHome,bd=0,padx=24,pady=18)
    fi_but.place(x=110,y=540)

def setOne5(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(5)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne6(1)
    red_but["command"]=lambda:setOne6(0)
    Label(text_space ,text="क्या आपके पेट में गुलाब के धब्बे हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/rosespots.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne4(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(4)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne5(1)
    red_but["command"]=lambda:setOne5(0)
    Label(text_space ,text="क्या आप पेट और शरीर के दर्द से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/abdominbodypain.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne3(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(3)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne4(1)
    red_but["command"]=lambda:setOne4(0)
    Label(text_space ,text="क्या आप अपनी भूख खो देते हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/appetite.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne2(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(2)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne3(1)
    red_but["command"]=lambda:setOne3(0)
    Label(text_space ,text="क्या आप रातों के दौरान पसीने से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/nightsweats.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setOne1(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(1)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setOne2(1)
    red_but["command"]=lambda:setOne2(0)
    Label(text_space ,text="क्या आपके शरीर का तापमान धीरे-धीरे बढ़ा है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/bodytempinc.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo6(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(8)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
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
        playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/seriousdisease.mp3"))
        Label(text_space ,text="आप गंभीर छूट के लक्षण हैं\nकृपया प्राथमिक स्वास्थ्य देखभाल केंद्र के पास जाएं।" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    else:
        prob=(c2/4)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Common Cold" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Common Cold)="+str("%0.2f" %prob) ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    Label(text_space ,text="आप "+str(len(covid19))+" Symptoms of COVID-19\nकिंडल टैग कोरोना टेस्ट" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/covid19.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/seriousdisease.mp3"))
    Label(text_space ,text="रिपोर्ट को ध्यान केंद्रित करने के लिए चिकित्सा सुविधा के लिए भेजा गया है" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    green_but.place_forget()
    red_but.place_forget()
    final_but = Button(chat_bot,text="दस्तावेज़ अपलोड करें",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=addDocuments,bd=0,padx=12,pady=10)
    final_but.place(x=110,y=470)
    fi_but = Button(chat_bot,text="समाप्ति",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=goToHome,bd=0,padx=24,pady=18)
    fi_but.place(x=110,y=540)

def setTwo5(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(6)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo6(1)
    red_but["command"]=lambda:setTwo6(0)
    Label(text_space ,text="क्या आप नाक बहने से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/runnynose.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo4(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(5)
        sec.append(7)
        covid19.append(6)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo5(1)
    red_but["command"]=lambda:setTwo5(0)
    Label(text_space ,text="क्या आपको अचानक वजन कम हुआ?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/suddenweight.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo3(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(3)
        sec.append(4)
        covid19.append(5)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo4(1)
    red_but["command"]=lambda:setTwo4(0)
    Label(text_space ,text="क्या आप हल्के या उच्च बुखार से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo2(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(2)
        covid19.append(4)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo3(1)
    red_but["command"]=lambda:setTwo3(0)
    Label(text_space ,text="क्या आपको शाम और रातों के दौरान सीने में दर्द और तापमान में वृद्धि होती है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setTwo1(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(1)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setTwo2(1)
    red_but["command"]=lambda:setTwo2(0)
    Label(text_space ,text="क्या आप गले में खराश से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    #playsound(os.path.join(os.path.dirname(__file__),"audio/nasal.mp3")) #abhi change this to sore throat
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree6(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(6)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
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
        Label(text_space ,text="आपके पास गैस्ट्रिक अल्सर और कृमि संक्रमण के दोनों लक्षण हैं" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/gastricworm.mp3"))
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
    Label(text_space ,text="आप गंभीर छूट के लक्षण हैं\nकृपया सार्वजनिक स्वास्थ्य देखभाल केंद्र के पास जाएं" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="रिपोर्ट को ध्यान केंद्रित करने के लिए चिकित्सा सुविधा के लिए भेजा गया है" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    green_but.place_forget()
    red_but.place_forget()
    final_but = Button(chat_bot,text="Upload Documents",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=addDocuments,bd=0,padx=12,pady=10)
    final_but.place(x=110,y=470)
    fi_but = Button(chat_bot,text="समाप्त",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=goToHome,bd=0,padx=24,pady=18)
    fi_but.place(x=110,y=540)

def setThree5(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(5)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree6(1)
    red_but["command"]=lambda:setThree6(0)
    Label(text_space ,text="क्या आप मसल क्रैम्प से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree4(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(4)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree5(1)
    red_but["command"]=lambda:setThree5(0)
    Label(text_space ,text="क्या आपको पेट में तेज दर्द है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree3(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(3)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree4(1)
    red_but["command"]=lambda:setThree4(0)
    Label(text_space ,text="क्या आप गुदा के आसपास खुजली से पीड़ित थे?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree2(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(2)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree3(1)
    red_but["command"]=lambda:setThree3(0)
    Label(text_space ,text="क्या आप मतली से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setThree1(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(1)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setThree2(1)
    red_but["command"]=lambda:setThree2(0)
    Label(text_space ,text="क्या आप मल से रक्त से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour7(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(7)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
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
        Label(text_space ,text="आप गंभीर छूट के लक्षण हैं\nकृपया सार्वजनिक स्वास्थ्य देखभाल केंद्र के पास जाएं।" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/seriousdisease.mp3"))
    else:
        prob=(c2/4)*100
        Label(text_space ,text="You are affected by" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="Dehydration" ,bg="#002C3E" , fg = "#008000", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="P(Dehydration)="+str("%0.2f" %prob) ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    
    Label(text_space ,text="आपका ध्यान के लिए निकटतम चिकित्सा सुविधा के लिए भेजा गया है" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/seriousdisease.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    green_but.place_forget()
    red_but.place_forget()
    final_but = Button(chat_bot,text="Upload Documents",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=addDocuments,bd=0,padx=12,pady=10)
    final_but.place(x=110,y=470)
    fi_but = Button(chat_bot,text="समाप्त",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=goToHome,bd=0,padx=24,pady=18)
    fi_but.place(x=110,y=540)

def setFour6(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(6)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour7(1)
    red_but["command"]=lambda:setFour7(0)
    Label(text_space ,text="क्या आप बेहोशी महसूस करते हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour5(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(5)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour6(1)
    red_but["command"]=lambda:setFour6(0)
    Label(text_space ,text="क्या आप भ्रम से ग्रस्त हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour4(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(4)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour5(1)
    red_but["command"]=lambda:setFour5(0)
    Label(text_space ,text="क्या आप सांस की तकलीफ से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/breathless.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour3(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(3)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour4(1)
    red_but["command"]=lambda:setFour4(0)
    Label(text_space ,text="क्या आपकी नाड़ी की दर सामान्य से अधिक है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/pulseratehigh.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour2(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(2)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour3(1)
    red_but["command"]=lambda:setFour3(0)
    Label(text_space ,text="क्या आपका मूत्र काला दिखता है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/urine.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def setFour1(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        sec.append(1)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:setFour2(1)
    red_but["command"]=lambda:setFour2(0)
    Label(text_space ,text="क्या आप थके हुए हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def startSecondary(n):
    if((2 in prime) and (3 in prime) and(4 in prime)):
        Label(text_space ,text="1. कंपकंपी के साथ उच्च बुखार?\n2. दिन भर तापमान में लगातार वृद्धि?\n3. रात को पसीना?\n4. भूख में कमी?\n5. पेट / शरीर का दर्द?\n6. पेट में गुलाब के धब्बे?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        Label(text_space ,text="क्या आप तेज बुखार से कांप रहे हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/shivering.mp3"))
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        green_but["command"]=lambda:setOne1(1)
        red_but["command"]=lambda:setOne1(0)
    elif(((1 in prime) and (2 in prime)) or ((2 in prime) and (5 in prime)) or ((5 in prime) and (1 in prime))):
        Label(text_space ,text="1. बढ़ी हुई थूक या रक्त के साथ खांसी?\n2. गले में खराश?\n3. सीने में दर्द और शाम और रात के दौरान तापमान में वृद्धि?\n4. हल्का बुखार?\n5. अचानक वजन कम होना?\n6. बहती नाक?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        Label(text_space ,text="क्या आपको बढ़े हुए थूक या खून से खांसी है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
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
        playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/heartburn.mp3"))
        Label(text_space ,text="क्या आप हार्ट बर्न या रिग्रिटेशन से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        green_but["command"]=lambda:setThree1(1)
        red_but["command"]=lambda:setThree1(0)
    elif((5 in prime) and (6 in prime)):
        Label(text_space ,text="1. अत्यधिक प्यास?\n2. थकान?\n3. गहरे रंग का पेशाब?\n4. तेजी से दिल की दर?\n5. सांस फूलना?\n6. भ्रम की स्थिति?\n7. बेहोशी के प्रकरण?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")

        Label(text_space ,text="क्या आप चरम प्यास से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        green_but["command"]=lambda:setFour1(1)
        red_but["command"]=lambda:setFour1(0)
    else:
        Label(text_space ,text="हैलो!! "+pat_Name +"\nआपको सिर्फ आम संक्रमण है ...\nस्वस्थ भोजन करें और थोड़ा आराम करें\nमेडिसिन टैब में बताई गई दवा लें",bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
        playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/commoninfec.mp3"))
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
        text_area.update()
        text_area.yview_moveto("1.0")
        green_but.place_forget()
        red_but.place_forget()
        final_but = Button(chat_bot,text="दस्तावेज़ अपलोड करें",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=addDocuments,bd=0,padx=12,pady=10)
        final_but.place(x=110,y=470)
        fi_but = Button(chat_bot,text="समाप्त",fg="#002C3E",bg="#fbd428",font=('Ubuntu',17,"bold"),
                        command=goToHome,bd=0,padx=24,pady=18)
        fi_but.place(x=110,y=540)
    

def getHead(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(6)
        covid19.append(3)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:startSecondary(1)
    red_but["command"]=lambda:startSecondary(0)
    Label(text_space ,text="डेटा का विश्लेषण...\nलक्षणों का माध्यमिक सेट तैयार हो रहा है!" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/secondarysymp.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    startSecondary(1)

def getDizzy(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(5)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getHead(1)
    red_but["command"]=lambda:getHead(0)
    Label(text_space ,text="क्या आप सिरदर्द से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/headache.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def getVomit(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(4)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getDizzy(1)
    red_but["command"]=lambda:getDizzy(0)
    Label(text_space ,text="क्या आप चक्कर से पीड़ित हैं?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/dizziness.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def getAbpain(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(3)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getVomit(1)
    red_but["command"]=lambda:getVomit(0)
    Label(text_space ,text="क्या आपको उल्टी हुई?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/vomit.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def getFever(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(2)
        covid19.append(2)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getAbpain(1)
    red_but["command"]=lambda:getAbpain(0)
    Label(text_space ,text="क्या आपको हिप या पेट दर्द है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/abdomenstomach.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")

def getCough(n):
    if(n==1):
        Label(text_space ,text="हाँ" ,bg="#008000" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
        prime.append(1)
        covid19.append(1)
    else:
        Label(text_space ,text="नहीं" ,bg="#7C0A02" , fg = "#FCF6F5", justify = LEFT , wraplength = 200, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="e")
        Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',5),padx=5,pady=5).pack(anchor="e")
    text_area.update()
    text_area.yview_moveto("1.0")
    time.sleep(1)
    green_but["command"]=lambda:getFever(1)
    red_but["command"]=lambda:getFever(0)
    Label(text_space ,text="क्या आपको बुखार है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/fever.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    text_area.update()
    text_area.yview_moveto("1.0")



def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def getSymptoms():
    try:
        two_frame.place_forget()
    except NameError:
        pass
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

    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/cliniconwelcome.mp3")) # 1.Hi I'm baju an inbuilt assistant 2. Press the button to respond
    Label(text_space ,text="नमस्ते, आप क्लिनिकन का उपयोग कर रहे हैं। अब आप सुरक्षित हैं। आइए हम आपकी बीमारी का निदान करते हैं!" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    #time.sleep(2)
    Label(text_space ,text="आइए निदान प्रक्रिया शुरू करें" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/procedure.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    #time.sleep(2)
    Label(text_space ,text="अपने प्राथमिक लक्षण चुनें" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/primarysymp.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")
    #time.sleep(2)
    Label(text_space ,text="क्या आपको खांसी है?" ,bg="#002C3E" , fg = "#FCF6F5", justify = LEFT, wraplength = 300, font=('Ubuntu',11,"bold"),padx=5,pady=5).pack(anchor="w")
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/cough.mp3"))
    Label(text_space ,text="" ,bg="#78Bfff" , fg = "#FCF6F5", justify = LEFT, wraplength = 200, font=('Ubuntu',1),padx=5,pady=5).pack(anchor="w")

def getTemp():
    dia_title["text"]="शरीर का तापमान"
    dia_image["image"]=step10
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/temp.mp3")) #Thermal Simulation
    time.sleep(2)
    thermalSimulation()
    dia_result["text"]="Simulated-ex: Temp - 97.5°C"
    namebut["command"]=getSymptoms

def getPhoto(n):
    try:
        invalid_but.place_forget()
    except NameError:
        pass
    if n==0:
        global pat_Aadhar
        if(pat_Aadhar=="" or len(pat_Aadhar)!=12):
            pat_Aadhar = dia_result["text"]

        if(len(pat_Aadhar)!=12):
            noti = ToastNotifier()
            noti.show_toast("CLINICON","Invalid Aadhar No",icon_path=icon_path,duration=3)
            getAadhar()
            return
    dia_title["text"]="फोटो खींची जा रही है"
    dia_image["image"]=step9
    #area to update db -- Weight
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/placeyourface.mp3")) #detecting face
    d_face=detectFace()
    if(d_face==1):
        dia_result["text"]="Face Detected"
        #playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/photocaptured.mp3")) #Face detected capturing Photo
    else:
        dia_result["text"]="चेहरा पहचान नहीं सकते ... फिर से शुरू"
        #playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/phototimeelapsed.mp3")) #Face Time Elapsed Trying Again
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
    dia_title["text"]="अपना वजन दर्ज करें (किलो में)"
    dia_image["image"]=step8
    #area to update db -- Height
    dia_result["text"]=""
    #playsound(os.path.join(os.path.dirname(__file__),"audio/weight.mp3"))

    namebut["command"]=lambda:getPhoto(1)



def getHeight():
    global pat_Contact
    if(pat_Contact=="" or len(pat_Contact)!=10):
        pat_Contact = dia_result["text"]

    if(len(pat_Contact)!=10):
        noti = ToastNotifier()
        noti.show_toast("CLINICON","Invalid Contact No",icon_path=icon_path,duration=3)
        getContact()
        return
    dia_title["text"]="अपनी ऊंचाई दर्ज करें (सेमी में)"
    dia_image["image"]=step7
    #area to update db -- Contact
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/height.mp3"))

    namebut["command"]=getWeight

def getContact():
    global pat_Age
    if(pat_Age=="" or int(pat_Age)<7 or int(pat_Age)>95):
        pat_Age = dia_result["text"]
    print(pat_Age)
    if(int(pat_Age)<7 or int(pat_Age)>95):
        noti = ToastNotifier()
        noti.show_toast("CLINICON","Age is not permitted or Invalid Age",icon_path=icon_path,duration=3)
        getAge()
        return
    dia_title["text"]="अपना संपर्क नंबर दर्ज करें"
    dia_image["image"]=step6
    #area to update db -- Aadhar
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/contact.mp3"))

    namebut["command"]=getHeight

def getAadhar():
    global pat_Age
    # if(pat_Age=="" or int(pat_Age)<7 or int(pat_Age)>95):
    #     pat_Age = dia_result["text"]
    # print(pat_Age)
    # if(int(pat_Age)<7 or int(pat_Age)>95):
    #     noti = ToastNotifier()
    #     noti.show_toast("CLINICON","Age is not permitted or Invalid Age",icon_path=icon_path,duration=3)
    #     getAge()
    #     return
    dia_title["text"]="अपना आधार नंबर दर्ज करें"
    dia_image["image"]=step5
    enableNumpad(number_pad.winfo_children())
    #area to update db -- Age
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/aadhar.mp3"))
    global invalid_but
    invalid_but = Button(dia_frame,text="मेरे पास आधार नहीं है",fg="#ffffff",bg="#000000",font=('Ubuntu',12,"bold"),
                        command=getName,bd=0,padx=24,pady=18)
    invalid_but.place(x=337,y=627)

    namebut["command"]=lambda:getPhoto(0)

def getAge():
    dia_title["text"]="अपनी आयु दर्ज करें"
    dia_image["image"]=step4
    girl_but.place_forget()
    boy_but.place_forget()
    enableNumpad(number_pad.winfo_children())
    #area to update db -- gender
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/age.mp3"))

    namebut["command"]=getContact

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
    dia_title["text"]="लिंग चुनें"
    dia_image["image"]=step3
    namebut.place_forget()
    retry_button.place_forget()
    #area to update db -- name
    dia_result["text"]=""
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/gender.mp3"))
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
    dia_title["text"]="कृपया अपना नाम बताएं"
    dia_image["image"]=step2
    invalid_but.place_forget()
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/name.mp3"))
    name=cliniconGetData("name")
    dia_result["text"]=name
    global pat_Name
    pat_Name=name
    wel1["text"]=(name+"\n")
    namebut["command"]=getGender
    retry_button.place(x=10,y=5)
    retry_button["command"]=getName
    if(name=="audio_error"):
        dia_result["text"]="तुम ठीक से नहीं सुन सकते"
        getName()
        return

    

def generateID():
    dia_title["text"]="अपनी आईडी नोट करें"
    dia_image["image"]=step1
    playsound(os.path.join(os.path.dirname(__file__),"hindiaudio/ID.mp3"))
    #logic to generate ID

    dia_result["text"]="CliniSIH207" #change with variable
    lab10["text"]="ID"
    lab11["text"]="CliniSIH207" #change with variable
    namebut["command"]=getAadhar
    retry_button.place_forget()
    disableNumpad(number_pad.winfo_children())
    
def dataAnalysis():
    global data_frame
    data_frame = LabelFrame(root,bg="#222831",relief=GROOVE)
    frame2.place_forget()
    data_frame.place(x=500,y=147,height=607,width=847)
    ctitle=Label(data_frame,text="डेटा विज़ुअलाइज़ेशन:",bg="#222831",fg="#ee3422",font=("Ubuntu",27),anchor=CENTER)
    ctitle.grid(row=0,column=0)
    g1=Label(data_frame,padx=5,pady=5,image=gr1)
    g1.grid(row=1,column=0)

def covidPrevent():
    pass
    global covid_frame
    covid_frame = LabelFrame(root,bg="#f2f2f2",relief=GROOVE)
    frame2.place_forget()
    covid_frame.place(x=500,y=147,height=607,width=847)
    ctitle=Label(covid_frame,text='"रोकथाम इलाज से बेहतर है"',bg="#ddf3f5",fg="#f6006b",font=("Ubuntu",27,"italic"),anchor=CENTER)
    ctitle.pack()
    content_frame=LabelFrame(covid_frame,bg="#000b29",relief=GROOVE)
    content_frame.pack(pady=5)
    pre_title=Label(content_frame,text="नकाब पहनिए। जीवन बचाए।",bg="#ddf3f5",fg="#000b29",font=("Ubuntu",29,"bold"),anchor=CENTER)
    pre_title.pack()
    pre_label=Label(content_frame,text="फेस कवर पहनें\nअपने हाथ धोएं\nसुरक्षित दूरी बनाए रखें",bg="#ddf3f5",fg="#000b29",font=("Ubuntu",25),anchor=CENTER)
    pre_label.pack()
    steps_pre=Label(covid_frame,text="के प्रसार को रोकने के लिए:\n1.अपने हाथों को अक्सर साफ करें। साबुन और पानी का उपयोग करें, या शराब आधारित हाथ रगड़ें।\n2.खांसी या छींकने वाले किसी से भी सुरक्षित दूरी बनाए रखें।\n3.जब शारीरिक गड़बड़ी संभव न हो तो मास्क पहनें।\n4.अपनी आंखों, नाक या मुंह को न छुएं।\n5.खांसने या छींकने पर अपनी नाक और मुंह को अपनी मुड़ी हुई कोहनी या एक ऊतक से ढक लें।\n6.यदि आप अस्वस्थ महसूस करते हैं तो घर पर रहें।\n7. यदि आपको बुखार, खांसी और सांस लेने में कठिनाई होती है, तो चिकित्सा पर ध्यान दें।",bg="#ddf3f5",fg="#000b29",font=("Ubuntu",14),anchor=CENTER)
    steps_pre.pack()

def startDiagnosing():
    try:
        check_frame.place_forget()
    except NameError:
        pass
    try:
        number_id.place_forget()
    except NameError:
        pass
    global dia_frame
    dia_frame = LabelFrame(root,bg="#fbd46d",relief=GROOVE)
    frame2.place_forget()
    dia_frame.place(x=277,y=107,height=707,width=657)
    global dia_title
    dia_title=Label(dia_frame,text="",bg="#222831",fg="#ddf3f5",font=("Ubuntu",30),anchor=CENTER)
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
    bclear=Button(number_pad,text="हटाना",fg="#ffffff",bg="#c41212",font=('Ubuntu',18,"bold"),bd=0,padx=30,pady=32,command=clear_value)

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


def startReport():
    try:
        two_frame.place_forget()
    except NameError:
        pass
    global re_frame
    re_frame = LabelFrame(root,bg="#222831",relief=GROOVE)
    re_frame.place(x=500,y=117,height=700,width=700)
    re_title=Label(re_frame,text="आपका प्रिस्क्रिप्शन",bg="#002C3E",fg="#ddf3f5",font=("Ubuntu",32),anchor=CENTER)
    re_title.pack()
    global dis_image
    dis_image=Label(re_frame,bg="#222831",image=ds1)
    dis_image.pack()
    id_t = Button(re_frame,text="प्रिन्ट",bg="#faca0f",fg="#ffffff",font=("Ubuntu",17,"bold"))
    id_t.pack(pady=2)

def twoOptions():
    try:
        check_frame.place_forget()
    except NameError:
        pass
    try:
        number_id.place_forget()
    except NameError:
        pass
    global two_frame
    two_frame = LabelFrame(root,bg="#002C3E",relief=GROOVE)
    two_frame.place(x=500,y=177,height=377,width=657)
    global two_title
    two_title=Label(two_frame,text="विकल्पों का चयन करें",bg="#002C3E",fg="#ddf3f5",font=("Ubuntu",32),anchor=CENTER)
    two_title.pack()
    id_two1 = Button(two_frame,text="मुझे न्यू डायग्नोसिस चाहिए",bg="#000000",fg="#ffffff",font=("Ubuntu",17,"bold"),padx=5,pady=5,command=getSymptoms)
    id_two1.pack(pady=27)
    id_two2 = Button(two_frame,text="अपनी रोग रिपोर्ट जानिए",bg="#000000",fg="#ffffff",font=("Ubuntu",17,"bold"),padx=5,pady=5,command=startReport)
    id_two2.pack(pady=17)

def ent(n):
    a = check_result.get()
    check_result.delete(0,END)
    check_result.insert(0,a+n)

def clear_id():
    check_result.delete(0,END)

def checkNewUser():
    frame2.place_forget()
    global check_frame
    check_frame = LabelFrame(root,bg="#222831",relief=GROOVE)
    check_frame.place(x=277,y=107,height=707,width=657)
    global check_title
    check_title=Label(check_frame,text=" क्या आपने क्लीनिकॉन बिफोर का इस्तेमाल किया है",bg="#222831",fg="#ddf3f5",font=("Ubuntu",30),anchor=CENTER,wraplength = 500)
    check_title.pack()
    global check_image
    check_image=Label(check_frame,bg="#222831",image=userid)
    check_image.pack()
    global check_result
    check_result=Entry(check_frame,text="",bg="#faca0f",fg="#000000",font=("Ubuntu",30),width=4)
    check_result.pack(pady=5)
    check_result.focus()
    id_next = Button(check_frame,text="प्रस्तुत",bg="#158dd4",fg="#ffffff",font=("Ubuntu",17,"bold"),padx=5,pady=5,command=twoOptions)
    id_next.pack(pady=5)
    id_new = Button(check_frame,text="नहीं, मैं एक नया उपयोगकर्ता हूं",bg="#000000",fg="#ffffff",font=("Ubuntu",17,"bold"),padx=5,pady=5,command=startDiagnosing)
    id_new.pack(pady=30)
    global number_id
    number_id = LabelFrame(root,bg="#222831",relief=GROOVE)
    number_id.place(x=967,y=107,height=527,width=370)
    b1=Button(number_id,text="1",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("1"),bd=0,padx=35,pady=30)
    b2=Button(number_id,text="2",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("2"),bd=0,padx=35,pady=30)
    b3=Button(number_id,text="3",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("3"),bd=0,padx=35,pady=30)
    b4=Button(number_id,text="4",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("4"),bd=0,padx=35,pady=30)
    b5=Button(number_id,text="5",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("5"),bd=0,padx=35,pady=30)
    b6=Button(number_id,text="6",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("6"),bd=0,padx=35,pady=30)
    b7=Button(number_id,text="7",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("7"),bd=0,padx=35,pady=30)
    b8=Button(number_id,text="8",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("8"),bd=0,padx=35,pady=30)
    b9=Button(number_id,text="9",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("9"),bd=0,padx=35,pady=30)
    b0=Button(number_id,text="0",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("0"),bd=0,padx=35,pady=30)
    bdot=Button(number_id,text=".",fg="#ffffff",bg="#000000",font=('Ubuntu',27,"bold"),command=lambda:ent("."),bd=0,padx=35,pady=30)
    bclear=Button(number_id,text="हटाना",fg="#ffffff",bg="#c41212",font=('Ubuntu',18,"bold"),bd=0,padx=30,pady=32,command=clear_id)

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


#contains menu
def nameFrame():
    global frame2
    frame2 = LabelFrame(root,bg="#222831",relief=GROOVE)
    frame2.place(x=500,y=147,height=550,width=700)
    l1=Button(frame2,text="स्टार्ट",bg="#f6006b",fg="#dae1e7",font=("Ubuntu",15,"bold"),padx=20,pady=20,width=20,command=checkNewUser)
    l2=Button(frame2,text="अपनी मेडिकल रिपोर्ट देखें",bg="#158dd4",fg="#dae1e7",font=("Ubuntu",17),padx=20,pady=20,width=20)
    l3=Button(frame2,text="एक चिकित्सक से परामर्श लें",bg="#158dd4",fg="#dae1e7",font=("Ubuntu",17),padx=20,pady=20,width=20,command=getSymptoms)
    l4=Button(frame2,text="डेटा जानकारी",bg="#158dd4",fg="#dae1e7",font=("Ubuntu",17),padx=20,pady=20,width=20,command=dataAnalysis)
    l5=Button(frame2,text="कैसे इस्तेमाल करे?",bg="#158dd4",fg="#dae1e7",font=("Ubuntu",17),padx=20,pady=20,width=20,command=addDocuments)
    l6=Button(frame2,text="अपनी दवा प्राप्त करें",bg="#2257bf",fg="#dae1e7",font=("Ubuntu",17),padx=20,pady=20,width=20)
    l7=Button(frame2,text="COVID-19 निवारक उपाय",bg="#e6c60d",fg="#ffffff",font=("Ubuntu",17,"bold"),padx=20,pady=20,command=covidPrevent)
    #frame1.place_forget()
    l1.grid(row=0,column=0,padx=20,pady=20)
    l2.grid(row=0,column=1,padx=20,pady=20)
    l3.grid(row=1,column=0,padx=20,pady=20)
    l4.grid(row=1,column=1,padx=20,pady=20)
    l5.grid(row=2,column=0,padx=20,pady=20)
    l6.grid(row=2,column=1,padx=20,pady=20)
    l7.grid(row=3,column=0,columnspan=2,padx=20,pady=20)


def welcomeFrame():
    global frame1
    frame1 = Frame(root,bg="#222831",relief=GROOVE)
    frame1.place(x=45,y=107,height=667,width=317)
    lab1=Label(frame1,text="नमस्ते!",bg="#222831",fg="#01b4f5",font=("Ubuntu",16),anchor=W)
    lab1.grid(row=0,column=0,sticky=W+E)
    global wel1
    wel1=Label(frame1,text="\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    wel1.grid(row=1,column=0,sticky=W+E)
    lab2=Label(frame1,text="तारीख",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab2.grid(row=2,column=0,sticky=W+E)
    lab3=Label(frame1,text=today.strftime("%B %d, %Y")+"\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab3.grid(row=3,column=0,sticky=W+E)
    lab4=Label(frame1,text="स्थानीय समय",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab4.grid(row=4,column=0,sticky=W+E)
    global lab5
    lab5=Label(frame1,text=now.strftime("%H:%M:%S")+"\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab5.grid(row=5,column=0,sticky=W+E)
    lab6=Label(frame1,text="डिवाइस आईडी",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab6.grid(row=6,column=0,sticky=W+E)
    lab7=Label(frame1,text="CLINI07AH\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab7.grid(row=7,column=0,sticky=W+E)
    lab8=Label(frame1,text="स्थान",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
    lab8.grid(row=8,column=0,sticky=W+E)
    lab9=Label(frame1,text="Dharavi/धारावी\n",bg="#222831",fg="#ffffff",font=("Ubuntu",16),anchor=W)
    lab9.grid(row=9,column=0,sticky=W+E)
    global net_image
    global net2
    net1=Label(frame1,text="इंटरनेट",bg="#222831",fg="#01b4f5",font=("Ubuntu",14,'underline'),anchor=W)
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
    #an_app=Button(frame1,padx=5,pady=5,image=android)
    #an_app.place(x=5,y=557)
    

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
    try:
        covid_frame.place_forget()
    except NameError:
        pass
    try:
        data_frame.place_forget()
    except NameError:
        pass
    try:
        doc_frame.place_forget()
    except NameError:
        pass
    try:
        check_frame.place_forget()
    except NameError:
        pass
    try:
        number_id.place_forget()
    except NameError:
        pass
    try:
        re_frame.place_forget()
    except NameError:
        pass
    try:
        two_frame.place_forget()
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
    #android=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/android.png")))
    gr1=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/gr1.png")))
    plus=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/plus.png")))
    upload_doc_image=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/doc.png")))
    userid=ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/userid.png")))
    ds1 = ImageTk.PhotoImage(pl.open(os.path.join(os.path.dirname(__file__),"pictures/prescriptions/anaemia.jpg")))

    home_button=Button(root,text="Home",bg="#ffffff",fg="#ffffff",font=("Ubuntu",5,"bold"),image=home_button_image,height=24,width=24,command=goToHome)
    home_button.place(x=1477,y=27)
    
    welcomeFrame()
    nameFrame()

    updateTime() #calling update time fn
    getInternetStatus() #Internet Status
    
    root.mainloop()

