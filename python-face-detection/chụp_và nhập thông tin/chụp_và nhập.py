import cv2
import tkinter as tk
from tkinter import simpledialog
root = tk.Tk()
root.withdraw()
name_of_user = simpledialog.askstring(title="Tên của bạn", prompt="Hãy nhập tên của bạn:")
root.geometry("800x600")
if name_of_user is not None:
    name = name_of_user.encode('Utf-8').decode('utf-8')
    cap = cv2.VideoCapture(0)
    scaling_factor = 0.5
    root.geometry("800x600")
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        cv2.imshow('Webcam', frame)
        c = cv2.waitKey(1)
        if ret and c == 13: # nhấn en tơ để chụp
            cv2.imwrite(name + '.png', frame)
            print('Chụp xong')
            break
    cap.release()
    cv2.destroyAllWindows()
