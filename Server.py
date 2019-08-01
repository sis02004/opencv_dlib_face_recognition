import socket
import cv2
import numpy as np
import time
import os
import threading
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
def receiving():
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
        conn.send(p_name.encode())
        print("sending")
        if not os.path.isdir(PATH+filedir):
            os.mkdir(PATH+filedir)

        #cv2.imwrite(os.path.join(PATH+filedir, filename), frame)
        cv2.imwrite(PATH+filedir+"/"+filename, frame)
        cv2.waitKey(1)
        #data를 디코딩한다.

def sending():
    print("ready to send")
    while True:
        data = p_name
        data = data.encode()
        conn.send(data)
  
HOST='192.168.0.99'
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
p_name = "9999"
  
threading._start_new_thread(receiving,())
threading._start_new_thread(sending,())

while True:
    pass
