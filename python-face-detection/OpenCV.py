from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pygame
from tkinter import messagebox
from tkinter import *
import pyautogui
import time
import smtplib
import random
import qrcode

#STEP1: Load anh tu thu vien
path = "pic2"
pathsave = "save(DiemDanh)"+datetime.now().strftime("%d-%m-%Y")+".csv"
pathsave1 = "save(AnNinhChungCu)"+datetime.now().strftime("%d-%m-%Y")+".csv"
images = []
className = []
mylist = os.listdir(path)

for cl in mylist:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])

#STEP2: ENCODING

def MaHoa(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnow = MaHoa(images)
print("MA HOA THANH CONG...100%")

def Save(name):
    with open(pathsave,"r+") as f:
        myDatalist = f.readlines()
        nameList = []
        for line in myDatalist:
            entry = line.split(",")
            nameList.append(entry[0])
        if (name not in nameList):
            now = datetime.now()
            dtstring = now.strftime("%H:%M:%S")
            dystring = now.strftime("%d/%m/%Y")
            f.writelines(f"\n{name},{dtstring},{dystring}")
    f.close()

def Save1(name):
    with open(pathsave1,"r+") as f:
        myDatalist = f.readlines()
        nameList = []
        for line in myDatalist:
            entry = line.split(",")
            nameList.append(entry[0])
        if (name not in nameList):
            now = datetime.now()
            dtstring = now.strftime("%H:%M:%S")
            dystring = now.strftime("%d/%m/%Y")
            f.writelines(f"\n{name},{dtstring},{dystring}")
    f.close()

#Doc ID nguoi dung
with open("Gmail.csv","r") as f:
    s = f.readlines()
    e = [] # số căn cước
    m = [] # email
    for line in s:
            entry = line.split(",")
            e.append(entry[0])
            m.append(entry[1])
    f.close()

#Khoi tao cua so
pygame.init()

screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("AN NINH TRƯỜNG THPT TP ĐIỆN BIÊN PHỦ")
Icon = pygame.image.load('thuvien/icon.png')
pygame.display.set_icon(Icon)
f = open(pathsave,"w")
f.write("Name,Time,Day")
f.close()
f = open(pathsave1,"w")
f.write("Name,Time,Day")
f.close()


GREY = (150,150,150)
BLACK = (0,0,0)
WHITE = (255,255,255)

running = True

# hiện cửa sổ lựa chọn
font = pygame.font.SysFont("Times New Roman",50)
text_1 = font.render('kiểm tra thông tin ', True, BLACK)
text_2 = font.render(datetime.now().strftime("%d-%m-%Y"), True, BLACK)
text_3 = font.render('đăng kí', True, BLACK)

while running: # lặp cho đến khi nào sai
    screen.fill(GREY) # tạo 1 màn hình nền xám còn lại là thiết lập màn hình không quan trọng
    mouse_x, mouse_y = pygame.mouse.get_pos() 
    pygame.draw.rect(screen,WHITE,(57,76,574,153))
    pygame.draw.rect(screen,WHITE,(57,270,574,153))
    screen.blit(text_1, (210,120))
    screen.blit(text_2,(1,1))
    screen.blit(text_3,(110,320))
    for event in pygame.event.get(): #Các sự kiện được xếp hàng. Khi một sự kiện mới xảy ra, nó sẽ được thêm vào cuối hàng đợi. Khi pygame.event.get được gọi, các sự kiện hiện có trong hàng đợi sẽ được trả về và hàng đợi được làm trống.
        if event.type == pygame.QUIT: # nếu kiểu của sự kiện mang kiểu thoát thì out vì running mang giá trị False
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if (event.button == 1): 
                if (mouse_x > 57 and mouse_x < 574) and (mouse_y > 76 and mouse_y < 320): # nếu con con trỏ chuột bấm vào cái 1 thì thực thi
                    print("Dang mo....")
                    #Khoi dong webcam
                    cap = cv2.VideoCapture(0) # khởi tạo biến mang giá trị của web cam
                    while True: # lặp vô hạn khi nào break thì dừng
                        ret, frame = cap.read() # ret sẽ đúng khi web cam chạy dc còn không không thì F frame mới là ghía trị mang khung hình của web cam
                        framS = cv2.resize(frame, (0,0), None,fx = 0.5, fy = 0.5) # kiểm tra bằng cách thay đổi khung hình và điều chỉnh thành đen trăng giúp so sánh ảnh trong pic 2
                        framS = cv2.cvtColor(framS, cv2.COLOR_BGR2RGB)
                        #Xac dinh vi tri cua khuon mat
                        facecurFrame = face_recognition.face_locations(framS)
                        encodecurFrame = face_recognition.face_encodings(framS)
                        for encodeFace, faceLoc in zip(encodecurFrame,facecurFrame): # tìm vị trí và mã hóa ảnh khuôn mặt
                            matches = face_recognition.compare_faces(encodeListKnow,encodeFace)
                            faceDis = face_recognition.face_distance(encodeListKnow,encodeFace)
                            matchIndex = np.argmin(faceDis)
                            if faceDis[matchIndex] < 0.40:
                                name = className[matchIndex].upper()
                                Save(name)
                            else:
                                name = "Unknow"
                                scr = pyautogui.screenshot(region=(0,0,650,500), imageFilename="Unknow(DiemDanh).png")
                            y1, x2, y2, x1 = faceLoc
                            y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
                            cv2.rectangle(frame,(x1,y1), (x2,y2), (0,255,0), 2)
                            cv2.putText(frame,name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        cv2.imshow('DIEM DANH - NHAN DIEN KHUON MAT (Nhan Q de thoat)', frame)
                        if cv2.waitKey(1) == ord("q"):
                            break
                    cap.release()
                    cv2.destroyAllWindows()

                if (mouse_x > 57 and mouse_x < 574) and (mouse_y > 272 and mouse_y < 421):
                    check = True
                    print("Quet mat...")
                    #Khoi dong webcam
                    cap = cv2.VideoCapture(0)
                    
                    c = True
                    while c:
                        ret, frame = cap.read()
                        framS = cv2.resize(frame, (0,0), None,fx = 0.5, fy = 0.5)
                        framS = cv2.cvtColor(framS, cv2.COLOR_BGR2RGB)
                        #Xac dinh vi tri cua khuon mat
                        facecurFrame =face_recognition.face_locations(framS)
                        encodecurFrame = face_recognition.face_encodings(framS)
                        for encodeFace, faceLoc in zip(encodecurFrame,facecurFrame):
                            matches = face_recognition.compare_faces(encodeListKnow,encodeFace)
                            faceDis = face_recognition.face_distance(encodeListKnow,encodeFace)
                            matchIndex = np.argmin(faceDis)
                            if faceDis[matchIndex] < 0.50:
                                name = className[matchIndex].upper()
                                Save1(name)
                            else:
                                name = "Unknow"
                                scr = pyautogui.screenshot(region=(0,0,650,500), imageFilename="Unknow(AnNinhChungCu).png")
                                check = False
                            y1, x2, y2, x1 = faceLoc
                            y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
                            cv2.rectangle(frame,(x1,y1), (x2,y2), (0,255,0), 2)
                            cv2.putText(frame,name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        cv2.imshow('Đăng kí - NHAN DIEN KHUON MAT (Nhan Q de thoat)', frame)
                        if cv2.waitKey(1) == ord("q"):
                            break
                    cap.release()
                    cv2.destroyAllWindows()
                    kl = e[0]
                    mail_address = "whitehathacker245@gmail.com"
                    password = "zhxa mhmn noek xnty"
                    message = MIMEMultipart()
                    message['From'] = mail_address
                    message['To'] = kl
                    message['Subject'] = "test code 23"
                    lower = "abcdefghijklmnopqrstuvwxyz"
                    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    numbers = "0123456789"
                    string = lower + upper + numbers
                    length = 8
                    ma = "".join(random.sample(string,length))
                    mail_content = '''Subject: Ma bao mat là :''' + ''''''+ma
                    def QRcode(id_cccd):
                        qr = qrcode.QRCode(version=1, box_size=10, border=5)
                        qr.add_data(id_cccd)
                        qr.make(fit=True)
                        img = qr.make_image(fill='black', back_color='white')
                        img.save("qrcode.png")  # Lưu hình ảnh QR code vào file
                    QRcode(e)
                    # Thêm nội dung email
                    body = mail_content
                    message.attach(MIMEText(body, 'plain'))
                    # Thêm hình ảnh QR code vào email
                    with open("qrcode.png", 'rb') as file:
                        img = MIMEImage(file.read())
                        img.add_header('Content-Disposition', 'attachment', filename="qrcode.png")
                        message.attach(img)
                    # Thiết lập server và gửi mail
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(mail_address, password)
                    text = message.as_string()
                    server.sendmail(mail_address, m[0], text)
                    server.quit()
                    # Xóa file hình ảnh QR code sau khi gửi email
                    os.remove("qrcode.png")
                    print("oke")
                    print("Quet ma QR...")
                    cap = cv2.VideoCapture(0)
                    qrc = cv2.QRCodeDetector()
                    c = True
                    # while c:
                    #     ret, frame = cap.read()
                    #     if ret:
                    #         ret_qr, decoded_infor, points, _ = qrc.detectAndDecodeMulti(frame)
                    #         if ret_qr:
                    #             for s, p in zip(decoded_infor,points):
                    #                 if s:
                    #                     # kl = e[0]
                    #                     # mail_address = "whitehathacker245@gmail.com"
                    #                     # password = "zhxa mhmn noek xnty"
                    #                     # message = MIMEMultipart()
                    #                     # message['From'] = mail_address
                    #                     # message['To'] = kl
                    #                     # message['Subject'] = "test code 23"
                    #                     # lower = "abcdefghijklmnopqrstuvwxyz"
                    #                     # upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    #                     # numbers = "0123456789"
                    #                     # string = lower + upper + numbers
                    #                     # length = 8
                    #                     # ma = "".join(random.sample(string,length))
                    #                     # mail_content = '''Subject: Ma bao mat là :''' + ''''''+ma
                    #                     # def QRcode(id_cccd):
                    #                     #     qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    #                     #     qr.add_data(id_cccd)
                    #                     #     qr.make(fit=True)
                    #                     #     img = qr.make_image(fill='black', back_color='white')
                    #                     #     img.save("qrcode.png")  # Lưu hình ảnh QR code vào file
                    #                     # QRcode(e)
                    #                     # # Thêm nội dung email
                    #                     # body = mail_content
                    #                     # message.attach(MIMEText(body, 'plain'))
                    #                     # # Thêm hình ảnh QR code vào email
                    #                     # with open("qrcode.png", 'rb') as file:
                    #                     #     img = MIMEImage(file.read())
                    #                     #     img.add_header('Content-Disposition', 'attachment', filename="qrcode.png")
                    #                     #     message.attach(img)
                    #                     # # Thiết lập server và gửi mail
                    #                     # server = smtplib.SMTP('smtp.gmail.com', 587)
                    #                     # server.starttls()
                    #                     # server.login(mail_address, password)
                    #                     # text = message.as_string()
                    #                     # server.sendmail(mail_address, m[0], text)
                    #                     # server.quit()
                    #                     # # Xóa file hình ảnh QR code sau khi gửi email
                    #                     # os.remove("qrcode.png")
                    #                     # print("oke")
                    #                     c = False
                    #                 else:
                    #                     pass
                    #             frame = cv2.polylines(frame, [p.astype(int)], True, (0,0,255),8)
                    cv2.imshow("QRCODE (Nhan Q de thoat)", frame)
                    if (cv2.waitKey(1) & 0xFF == ord('q')):
                        break
                    cv2.destroyAllWindows()
                    root = Tk()
                    code = StringVar()
                    root.title('Nhap ma:')
                    root.geometry("150x150")
                    
                    entry = Entry(root,font='arial 15',bg = 'white',fg='black',bd = 4,width=40)
                    entry.place(x=1,y=1)
                    def get():
                        global running
                        data = entry.get()
                        if (data == ma) and (check == True):
                            print("Moi vao...")
                            running = False
                        else:
                            print("Nguoi la, moi di ra...")
                            running = False
                    btn = Button(root,text="Nhap",command = get)
                    btn.place(x=50,y=50)
                    root.mainloop()
    pygame.display.flip()
pygame.quit()