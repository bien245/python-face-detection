from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
# import pystray
# from PIL import Image
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pygame
import tkinter as tk
from tkinter import simpledialog
from tkinter import *
import pyautogui
import time
import smtplib
import random
import qrcode
import dlib
#STEP1: Load anh tu thu vien
path = "picture"
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
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h - 60
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("AN NINH TRƯỜNG THPT TP ĐIỆN BIÊN PHỦ")
Icon = pygame.image.load('icon/icon.png')
# image = Image.open("thuvien/icon.png")
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
hidden = True
running = True
# hiện cửa sổ lựa chọn

font = pygame.font.SysFont("Times New Roman",50)
text_1 = font.render('Quét mặt', True, BLACK)
text_2 = font.render(datetime.now().strftime("%d-%m-%Y"), True, BLACK)
text_3 = font.render('đăng kí', True, BLACK)

width, height = 650,500
show = True
while running:
    screen.fill(GREY)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, WHITE, (57, 76, 574, 153))
    pygame.draw.rect(screen, WHITE, (57, 270, 574, 153))

    screen.blit(text_1, (210, 120))
    screen.blit(text_2, (1, 1))
    screen.blit(text_3, (110, 320))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 57 < mouse_x < 574 and 76 < mouse_y < 320:
                    def MaHoa(images):
                        encodeList = []
                        for img in images:
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            encode = face_recognition.face_encodings(img)[0]
                            encodeList.append(encode)
                        return encodeList
                    encodeListKnow = MaHoa(images)
                    cap = cv2.VideoCapture(0)
                    if show:
                        # text_1 = font.render("Dang mo....", True, WHITE)
                        # text_2 = font.render("Nhấn Q để thoát", True, WHITE)
                        # text_3 = font.render("Nhan Q de thoat", True, WHITE)
                        screen.blit(text_1, (210, 120))
                        screen.blit(text_2, (1, 1))
                        screen.blit(text_3, (110, 320))
                    show = False
                    while True:
                        ret, frame = cap.read()
                        frame = cv2.resize(frame, (width, height))
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        face_locations = face_recognition.face_locations(frame)
                        face_encodings = face_recognition.face_encodings(frame, face_locations)
                        for face_location, face_encoding in zip(face_locations, face_encodings):
                            matches = face_recognition.compare_faces(encodeListKnow, face_encoding)
                            face_dis = face_recognition.face_distance(encodeListKnow, face_encoding)
                            match_index = np.argmin(face_dis)
                            if face_dis[match_index] < 0.40:
                                name = className[match_index]
                                Save(name)
                            else:
                                name = "Unknow"
                                scr = pyautogui.screenshot(region=(0, 0, width, height), imageFilename="Unknow(DiemDanh).png")
                            def draw_points(frame, landmarks, start, end, is_closed=False):
                                points = [landmarks.part(i) for i in range(start, end+1)]
                                for i in range(len(points)-1):
                                    cv2.line(frame, (points[i].x, points[i].y), (points[i+1].x, points[i+1].y), (0, 255, 0), 1)
                                if is_closed:
                                    cv2.line(frame, (points[-1].x, points[-1].y), (points[0].x, points[0].y), (0, 255, 0), 1)
                            y1, x2, y2, x1 = face_location
                            detector = dlib.get_frontal_face_detector()
                            predictor = dlib.shape_predictor("C:/Users/white.DESKTOP-GJ9453F/Downloads/shape_predictor_68_face_landmarks_GTX.dat/shape_predictor_68_face_landmarks_GTX.dat") # đường dẫn đến file pretrained
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            faces = detector(gray)
                            for face in faces:
                                landmarks = predictor(gray, face)
                                draw_points(frame, landmarks, 0, 16)
                                draw_points(frame, landmarks, 17, 21)
                                draw_points(frame, landmarks, 22, 26)
                                draw_points(frame, landmarks, 27, 30)
                                draw_points(frame, landmarks, 30, 35, True)
                                draw_points(frame, landmarks, 36, 41, True)
                                draw_points(frame, landmarks, 42, 47, True)
                                draw_points(frame, landmarks, 48, 59, True)
                                draw_points(frame, landmarks, 60, 67, True)
                            cv2.putText(frame,name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        frame = cv2.flip(frame, 0)
                        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                        pygame_surface = pygame.surfarray.make_surface(frame)
                        screen.blit(pygame_surface, (704,95))  
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                    cap.release()
                    cv2.destroyAllWindows()

                if (mouse_x > 57 and mouse_x < 574) and (mouse_y > 272 and mouse_y < 421):
                    check = True
                    print("Quet mat...")
                    root = tk.Tk()
                    root.withdraw()
                    name_of_user = simpledialog.askstring(title="Tên của bạn", prompt="Hãy nhập tên của bạn:")
                    if name_of_user is not None:
                        name = name_of_user.encode('Utf-8').decode('utf-8')
                        cap = cv2.VideoCapture(0)
                        scaling_factor = 0.5
                        root.geometry("800x600")
                        while True:
                            ret, camdki = cap.read()
                            if not ret:
                                break
                            camdki = cv2.resize(camdki, (width, height))
                            camdki = cv2.rotate(camdki, cv2.ROTATE_90_COUNTERCLOCKWISE)
                            camdki = cv2.cvtColor(camdki, cv2.COLOR_BGR2RGB)
                            pygame_surface = pygame.surfarray.make_surface(camdki)
                            screen.blit(pygame_surface, (704,95))  
                            pygame.display.flip() 
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                    cv2.imwrite("pic2/"+name + '.png', cv2.cvtColor(np.rot90(camdki, k =-1), cv2.COLOR_BGR2RGB))
                                    print('Chup xong')
                                    cap.release()
                                    pygame.quit()
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
                    body = mail_content
                    message.attach(MIMEText(body, 'plain'))
                    with open("qrcode.png", 'rb') as file:
                        img = MIMEImage(file.read())
                        img.add_header('Content-Disposition', 'attachment', filename="qrcode.png")
                        message.attach(img)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(mail_address, password)
                    text = message.as_string()
                    server.sendmail(mail_address, m[0], text)
                    server.quit()
                    os.remove("qrcode.png")
                    print("oke")
                    print("Quet ma QR...")
                    cap = cv2.VideoCapture(0)
                    qrc = cv2.QRCodeDetector()
                    c = True
                    while c:
                        ret, frame = cap.read()
                        if ret:
                            ret_qr, decoded_infor, points, _ = qrc.detectAndDecodeMulti(frame)
                            if ret_qr:
                                for s, p in zip(decoded_infor,points):
                                    frame = cv2.polylines(frame, [p.astype(int)], True, (0,0,255),8)
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
                            exit()
                        else:
                            print("Nguoi la, moi di ra...")
                            exit()
                    btn = Button(root,text="Nhap",command = get)
                    btn.place(x=50,y=50)
                    root.mainloop()
    pygame.display.flip()
pygame.quit()



