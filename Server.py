import socket
import cv2
import numpy as np
import time
import os
from datetime import datetime
from PIL import Image
from multiprocessing import Process, Queue
from datetime import datetime

#socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def getImagesAndLabels(PATH):
    file_list = [file for file in os.listdir(PATH) if not (file.endswith(".jpg") or file.endswith(".yml"))]
      
    faceSamples=[]
    ids = []
    for filePath in file_list :
        img_list = [file for file in os.listdir(PATH+filePath)]
        id = int(filePath.split("_")[1])
        
        for imagePath in img_list:
            PIL_img = Image.open(PATH+filePath+"/"+imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            faceSamples.append(img_numpy)
            ids.append(id)
    return faceSamples,ids

def train():
    
    PATH= r"C:/Users/SB/Desktop/face2/"
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    FILE="trainer.yml"

    HOST='192.168.0.4'
    PORT2=8001
    
    
    while True:
        time = int(datetime.today().hour)
        if time%23 == 0:
            #TCP 사용
            s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket2 created')
 
            #서버의 아이피와 포트번호 지정
            s2.bind((HOST,PORT2))
            print('Socket2 bind complete')
            # 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
            s2.listen(10)
            print('Socket2 now listening')
            #연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
            conn,addr=s2.accept()
            data_transferred = 0
            
            print ("Training faces. It will take a few seconds. Wait ...")
            faces,ids = getImagesAndLabels(PATH)
            recognizer.train(faces, np.array(ids))
            # Save the model into trainer/trainer.yml
            recognizer.save(PATH+FILE) # recognizer.save() worked on Mac, but not on Pi
            # Print the numer of faces trained and end program
            print("{0} faces trained. Exiting Program".format(len(np.unique(ids))))

            print("File transfer start...")
            with open(PATH+FILE,'rb') as f:
                try:
                    data = f.read(1024) # 파일을 1024바이트 읽음
                    while data: # 파일이 빈 문자열일때까지 반복
                        data_transferred += conn.send(data)
                        data = f.read(1024)
                    conn.close()
                except Exception as e:
                    print(e)
            print('전송완료[%s], 전송량[%d]' %(FILE,data_transferred))

def server():
    HOST='192.168.0.4'
    PORT=8000
    PATH = "C:/Users/SB/Desktop/face/"
    #TCP 사용
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')
 
    #서버의 아이피와 포트번호 지정
    s.bind((HOST,PORT))
    print('Socket bind complete')
    # 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
    s.listen(10)
    print('Socket now listening')
 
    #연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
    conn,addr=s.accept()
    i =0
    while True:
    # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
        print("receving")
        person_name = conn.recv(4)
        p_name = person_name.decode()
        length = recvall(conn, 12)
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype = 'uint8')
        #data를 디코딩한다.
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow',frame)

        filename = datetime.now().strftime("SB%Y%m%d_%H%M%S")+"_"+str(i)+".jpg"
        filedir = datetime.now().strftime("SB_"+str(p_name))
        print(p_name)
        print(filename)

        if not os.path.isdir(PATH+filedir):
            i = 0
            os.mkdir(PATH+filedir)

        #cv2.imwrite(os.path.join(PATH+filedir, filename), frame)
        cv2.imwrite(PATH+filedir+"/"+filename, frame)
        cv2.waitKey(1)
        i+=1
        #data를 디코딩한다.
    
if __name__ == '__main__':
    process_one = Process(target=server, args=())
    process_two = Process(target=train, args=())
    process_one.start()
    process_two.start()
    process_one.join()
    process_two.join()
