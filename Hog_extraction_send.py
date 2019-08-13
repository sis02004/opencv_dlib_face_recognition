from picamera.array import PiRGBArray
from picamera import PiCamera
import dlib
import cv2
import time
import socket
import io
import numpy
import os
#-*-coding:utf-8 -*-
from gtts import gTTS
import openface.openface.align_dlib as openface
import sys
from multiprocessing import Process, Queue
import threading
import subprocess
from datetime import datetime
from tkinter import *
from tkinter import ttk

#ID와 이름, 인식 여부 저장
name = dict()
id = ""
timeR = datetime.now()
from multiprocessing import Process, Queue

def recv_yml():
    HOST='192.168.0.4'
    PORT2=8001
    PATH="/home/pi/Downloads/"
    FILE='trainer.yml'
    
    while True:
        client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket2.connect((HOST, PORT2))
        fwrite=open(os.path.join(PATH,FILE),"w+")
        while True:
            data = client_socket2.recv(1024)
            if not data:
                break
            fwrite.write(data.decode("utf-8"))
        fwrite.close()
        client_socket2.close()
        print('File transfer complete')
    
#통근확인 버튼을 클릭하면 실행된다.
#출근 현황을 새로운 창을 통해 출력하는 함수
def showK(root) :
    #새로운 창 생성
    toplevel = Toplevel(root)
    toplevel.geometry("180x150")
    
    text = "\t  출근확인\t\t\n\n"
    names = list()
    
    for i in name.keys() :
        names.append(name[i][0])
    
    #이름순으로 인식 여부에 따라 출근 현황 출력
    names.sort()
    for i in names :
        for k in name :
            if name[k][0] == i :
                if name[k][1] :
                    text = text + name[k][0] + "\t근무 중\n"
                else :
                    text = text + name[k][0] + "\t확인불가\n"
    
    scrollbar = Scrollbar(toplevel)
    scrollbar.pack(side="right", fill="y")      
    label = Label(toplevel, text=text)
    label.pack()
    
#새롭게 이름과 아이디를 등록하고 얼굴을 등록하고자 할 경우 등록하기 버튼을 클릭하면 실행된다.
#이름을 등록하고 아이디를 부여하기 위한 새로운 창을 생성하는 함수
def makeU(root, q2, q3) :
    #새로운 창 생성
    toplevel = Toplevel(root)
    toplevel.geometry("180x75")
    toplevel.resizable(False, False)
    
    #음성파일 생성 및 실행
    if not os.path.exists("/home/pi/Project/mp3/name.mp3") :
        text = "이름을 입력해주세요."
        tts = gTTS(text, lang='ko')
        tts.save("/home/pi/Project/mp3/name.mp3")
    subprocess.call("mpg321 /home/pi/Project/mp3/name.mp3", shell=True)
    
    labelt = Label(toplevel,text="이름을 입력해주세요.",justify="center")
    labelt.pack()
    entryt = Entry(toplevel,bd=1,width=15)
    entryt.pack(side="left")
    #입력 버튼을 클릭하면 giveID 함수 실행
    buttont = ttk.Button(toplevel, text="입력", width=5, command = lambda:giveID(labelt, entryt, q2, q3))
    buttont.pack(side="right")
    
#아이디와 이름을 등록 및 저장하고
#서버가 얼굴을 등록하기 위한 신호 전송
def giveID(label, entry, q2, q3) :
    #entry로부터 입력받은 이름 저장
    user = entry.get()
    
    #entry 내용 삭제
    entry.delete(0, END)
    num = list()
    
    #1111부터 순서대로 아이디 부여
    for i in name.keys() :
        num.append(i)
    num.sort(reverse=True)
    idT = int(num[0])+1
    
    #아이디 및 이름 등록
    name[str(idT)]=[user, 0]
    file = open("/home/pi/Project/name.txt", 'a')
    file.write(str(idT)+","+user+"\n")
    file.close()
    
    #음성파일 생성 및 실행
    if not os.path.exists("/home/pi/Project/mp3/camera.mp3") :
        text = "이름이 등록되었습니다. 얼굴 등록을 위해 5분간 카메라를 바라봐주세요."
        tts = gTTS(text, lang='ko')
        tts.save("/home/pi/Project/mp3/camera.mp3")
    subprocess.call("mpg321 /home/pi/Project/mp3/camera.mp3", shell=True)
    label.configure(text="얼굴 등록을 위해\n5분간 카메라를 바라봐주세요.\n 남은 시간 : 5분")
    q2.put(str(idT))
    q3.put(str(idT))
    
    #1분 단위로 화면에 남은시간 표시
    for i in range(4) :
        time.sleep(60)
        label.configure(text="얼굴 등록을 위해\n5분간 카메라를 바라봐주세요.\n남은 시간 : "+str(4-i)+"분")
    time.sleep(60)

    temp = q3.get()
    #음성파일 생성 및 실행
    if not os.path.exists("/home/pi/Project/mp3/done.mp3") :
        text = "등록이 완료되었습니다."
        tts = gTTS(text, lang='ko')
        tts.save("/home/pi/Project/mp3/done.mp3")
    subprocess.call("mpg321 /home/pi/Project/mp3/done.mp3", shell=True)
    label.configure(text=name[str(idT)][0]+" 님의 등록번호는\n"+str(idT)+"입니다.")
    timeR = datetime.now()
    
#서버에 아이디는 저장되어 있으나 라즈베리에 이름이 등록되어 있지 않은 경우
#entry에 이름을 입력하고 버튼을 클릭하면 아이디 및 이름 등록
def enterName(label) :
    user = entry.get()
    entry.delete(0, END)
    
    #entry의 내용에 따라 아이디 및 이름 등록
    if user.upper() != "N" and user != "":
        name[id]=[user, 0]
        file = open("/home/pi/Project/name.txt", 'a')
        file.write(id+","+user+"\n")
        file.close()
        label.configure(text=name[id][0]+" 님의 등록번호는\n"+id+"입니다.")
        timeR = datetime.now()
    else :
        pass

#등록된 사람이 처음 감지되었을 때 음성파일을 실행하는 함수
def speech(id, name, label) :
    if not os.path.exists("/home/pi/Project/mp3/"+id+".mp3") :
        text = name[id][0]+" 님 좋은 하루 보내세요."
        tts = gTTS(text, lang='ko')
        tts.save("/home/pi/Project/mp3/"+id+".mp3")
    subprocess.call("mpg321 /home/pi/Project/mp3/"+id+".mp3", shell=True)
    label.configure(text=name[id][0]+" 님 좋은 하루 보내세요.\n"+datetime.now().strftime("%y/%m/%d %H:%M:%S"))
    
#등록되지 않은 사람이 감지되었을 때 음성파일을 실행하는 함수
def speechUn(id) :
    #등록되지 않은 사람이거나 카메라로부터 멀리 위치한 경우
    if id.startswith('9') :
        if not os.path.exists("/home/pi/Project/mp3/"+id+".mp3") :
            if id.endswith('0') :
                text = "앞으로 다가와 주세요."
            elif id.endswith('9') :
                text = "등록이 필요합니다."
            else :
                text = "오류"
            tts = gTTS(text, lang='ko')
            tts.save("/home/pi/Project/mp3/"+id+".mp3")
        subprocess.call("mpg321 /home/pi/Project/mp3/"+id+".mp3", shell=True)
    #서버에 아이디가 저장되어있으나 라즈베리에 이름은 등록되지 않은 경우
    else :
        if not os.path.exists("/home/pi/Project/mp3/Unknown.mp3") :
            text = "이름 등록이 필요합니다. 이름을 화면에 입력 후, 엔터키를 눌러주세요."
            tts = gTTS(text, lang='ko')
            tts.save("/home/pi/Project/mp3/Unknown.mp3")
        subprocess.call("mpg321 /home/pi/Project/mp3/Unknown.mp3", shell=True)
        
#서버로부터 인식된 사람의 아이디를 전송받는 함수
#아이디에 따라 적절한 액션 수행
def recvID(q, label) :  
    global name
    global id
    global timeR
    
    #아이디 및 이름이 등록된 파일을 불러와 변수 name 초기화
    file = open("/home/pi/Downloads/name.txt", 'r')
    while True :
        line = file.readline()
        if not line :
            break
        name[line.split(",")[0]] = [(line.split(",")[1]).split("\n")[0], 0]
    file.close()
    
    #음성파일의 재생 횟수를 제어하기 위한 변수
    checkT = 0

    while True :
        #하루 단위로 인식 여부 초기화
        if int((datetime.now()-timeR).days) > 0 :
            for i in name.keys() :
                name[i][1] = 0
        #30초 단위로 라벨 표시 삭제
        if int((datetime.now()-timeR).seconds) > 30 :
            label.configure(text="")
        try :   
            if q.qsize() > 0 :
                id = q.get()
                if not id :
                    break
                #등록되지 않은 사람이거나 카메라로부터 멀리 위치한 경우
                if int(id) // 9000 == 1:
                    #음성파일이 계속해서 실행되는 것을 막기 위해 3번에 한 번씩만 실행
                    checkT += 1
                    if checkT == 1 :
                        speechUn(id)
                        timeR = datetime.now()
                    elif checkT == 4 :
                        checkT = 0
                #등록된 사람이나 처음 인식된 경우
                #이미 인식된 경우는 음성파일을 실행할 필요가 없으므로 배제
                elif [k for k in name.keys() if k==id] and not name[id][1] :
                    speech(id, name, label)
                    #인식되었음을 표시
                    name[id][1] = 1
                    timeR = datetime.now()
                #서버에 아이디가 저장되어 있으나 라즈베리에 이름이 등록되지 않은 경우
                elif not [k for k in name.keys() if k==id] :
                    speechUn(id)
                    label.configure(text="등록을 원하지 않을 경우,\nN 또는 n을 입력 후 입력을 눌러주세요.")
                    timeR = datetime.now()
                    while True :
                        #이름을 입력하는 동안 음성파일이 실행되는 것을 막기 위해 loop
                        if int((datetime.now()-timeR).seconds) > 5 :
                            break
        except :
            pass

def tts(q,q2,q3):
    root = Tk()
    root.title("통근관리")
    root.geometry("200x85")
    root.resizable(False, False)

    frame1 = Frame(root)
    frame1.pack(side="top")
    frame2 = Frame(root)
    frame2.pack(side="bottom")

    button1 = ttk.Button(frame1, text="통근확인", command = lambda:showK(root))
    button1.pack(side="left")
    button2 = ttk.Button(frame1, text="등록하기", command = lambda:makeU(root, q2, q3))
    button2.pack(side="right")

    label = Label(frame2,text="",justify="center")
    label.pack()
    entry = Entry(frame2,bd=1,width=15)
    entry.pack(side="left")
    button3 = ttk.Button(frame2, text="입력", width=5, command = lambda:enterName(label))
    button3.pack(side="right")

#스레드를 통해 UI와 별개로 실행
    t = threading.Thread(target=recvID, args=(q,label, ))
    t.start()

    root.mainloop()
    t.join()

def camera(client_socket, q, q2, q3):
    camera = PiCamera()

    camera.resolution = (640,480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640,480))
    rec=cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(r"/home/pi/Downloads/trainer2.yml") :
        rec.read(r"/home/pi/Downloads/trainer2.yml")
    predictor_model = "/home/pi/Downloads/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    face_pose_predictor = dlib.shape_predictor(predictor_model)
    face_aligner = openface.AlignDlib(predictor_model)
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        vis = img.copy()
    
        for i, d in enumerate(rects) :
            cv2.rectangle(vis, (d.left(), d.bottom()), (d.right(), d.top()), (0, 255, 0), 2)
            #when a person is detected, the frame number and the order of the person are stored in grayscale

            if not (d.top()>0 and d.bottom()>0 and d.left()>0 and d.right()>0) :
                continue
            pose_landmarks = face_pose_predictor(gray, d)
            alignedFace = face_aligner.align(534, gray, d, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            result , image = cv2.imencode(".jpg", alignedFace, params=[cv2.IMWRITE_JPEG_QUALITY,100])
            id,conf=rec.predict(alignedFace)
            if(conf < 45):
                cv2.putText(vis, str(id)+" : "+str(round(conf,2)), (d.left(), d.bottom()), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 0))
            
            else:
                cv2.putText(vis, str(id)+" : "+str(round(conf,2)), (d.left(), d.bottom()), cv2.FONT_HERSHEY_PLAIN, 0.9, (0, 0, 255))
                id = 9999
            data = numpy.array(image)
            stringData = data.tostring()
            personal_id = str(id)
            if personal_id == "9999" and q3.qsize() > 0 :
                personal_id = q2.get()
                q2.put(personal_id)
            else :
                q.put(personal_id)
            client_socket.sendall((personal_id+(str(len(stringData)))).encode().ljust(16) + stringData)
        
        cv2.imshow("Frame", vis)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
    
        #if no person is detected, continue
        if len(rects) == 0:
            continue

        #exit when ESC is input
        if key == 27:
            cv2.destroyWindow()
            break

if __name__ == '__main__':
    q = Queue()
    q2 = Queue()
    q3 = Queue()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.0.4', 8000))
    process_one = Process(target=camera, args=(client_socket,q,q2,q3, ))
    process_two = Process(target=tts, args=(q,q2,q3, ))
    process_three = Process(target=recv_yml, args=())
    process_one.start()
    process_two.start()
    process_three.start()
    process_one.join()
    process_two.join()
    process_three.join()
