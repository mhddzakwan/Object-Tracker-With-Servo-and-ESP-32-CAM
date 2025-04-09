import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import serial
import time

last_sent = 0

win = Tk()
win.geometry("850x800+300+30")

color = "#581845"
frame_1 = Frame(win, width=850, height=800, bg=color).place(x=0, y=0)

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()
var6 = IntVar()
var7 = IntVar()
var8 = IntVar()

W = 150
l_h = Scale(frame_1, label="l_h", from_=0, to=255, orient=HORIZONTAL, variable=var1, activebackground='#339999')
l_h.set(0)
l_h.place(x=10, y=10, width=W)
l_s = Scale(frame_1, label="l_s", from_=0, to=255, orient=HORIZONTAL, variable=var2, activebackground='#339999')
l_s.set(0)
l_s.place(x=170, y=10, width=W)
l_v = Scale(frame_1, label="l_v", from_=0, to=255, orient=HORIZONTAL, variable=var3, activebackground='#339999')
l_v.set(0)
l_v.place(x=330, y=10, width=W)

u_h = Scale(frame_1, label="u_h", from_=255, to=0, orient=HORIZONTAL, variable=var4, activebackground='#339999')
u_h.set(255)
u_h.place(x=10, y=80, width=W)
u_s = Scale(frame_1, label="u_s", from_=255, to=0, orient=HORIZONTAL, variable=var5, activebackground='#339999')
u_s.set(255)
u_s.place(x=170, y=80, width=W)
u_v = Scale(frame_1, label="u_v", from_=255, to=0, orient=HORIZONTAL, variable=var6, activebackground='#339999')
u_v.set(255)
u_v.place(x=330, y=80, width=W)

Area = Scale(frame_1, from_=200, to=5000, orient=VERTICAL, variable=var7, activebackground='#339999')
Area.set(300)
Area.place(x=490, y=10, height=130)
act = Scale(frame_1, from_=100, to=500, orient=VERTICAL, variable=var8, activebackground='#339999')
act.set(100)
act.place(x=550, y=10, height=130)
ip_cam_url = "http://192.168.220.211:81/stream"  # Sesuaikan dengan IP ESP32-CAM
# ip_cam_url = "rtsp://192.168.42.1:554/live"  # Sesuaikan dengan IP ESP32-CAM
cap = cv2.VideoCapture(ip_cam_url)



label1 = Label(frame_1)
label2 = Label(frame_1)
label3 = Label(frame_1)
co = Label(frame_1, bg="#581845", fg='white')

Xposition = 90
Yposition = 90


ser = serial.Serial('COM13', '38400', timeout=5)
# ser = serial.Serial('COM11', '9600', timeout=5)
def toSerial(img,x, y):

    global Xposition, Yposition,last_sent
    rows, cols, _ = img.shape

    center_x = int(rows / 2)
    center_y = int(cols / 2)

    medium_x = int(x+5)
    medium_y = int(y+5)

    v=2
    m=60

    if medium_x > center_x + m:
        Xposition += v
        if Xposition>= 180:
            Xposition = 180

    if medium_x < center_x - m:
        Xposition -= v
        if Xposition < 0:
            Xposition = 0
#######################################
    if medium_y > center_y + m:
        Yposition += v
        if Yposition>= 180:
            Yposition = 180


    if medium_y < center_x - m:
        Yposition -= v
        if Yposition < 0:
            Yposition = 0
    current_time = time.time()
    if current_time - last_sent >= 0.4:  # 400 ms = 0.4 detik
        ser.write(('a' + str(int(Xposition)) + 'b' + str(int(Yposition))).encode())
        last_sent = current_time

def to_pil(img, label, x, y, w, h):
    img = cv2.resize(img, (w, h))
    image = Image.fromarray(img)
    iago = ImageTk.PhotoImage(image)
    label.configure(image=iago)
    label.image = iago
    label.place(x=x, y=y)

def to_pil2(img, label, x, y):
    image = Image.fromarray(img)
    iago = ImageTk.PhotoImage(image)
    label.configure(image=iago)
    label.image = iago
    label.place(x=x, y=y)

def get_frame():
    global cap
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        yield frame

frame_generator = get_frame()

def select_img():
    img = next(frame_generator)
    img = cv2.flip(img, 1)
    #img = cv2.resize(img, (520, 520))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # l_b = np.array([l_h.get(), l_s.get(), l_v.get()])
    # u_b = np.array([u_h.get(), u_s.get(), u_v.get()])
    l_b = np.array([162 , 121 , 48])
    u_b = np.array([209 , 255 , 255])
    # print(l_h.get(), ',', l_s.get(), ',', l_v.get(), ',', u_h.get(), ',', u_s.get(), ',', u_v.get())

    mask = cv2.inRange(hsv, l_b, u_b)
    kernal = np.ones((5, 5), "uint8")
    color = cv2.dilate(mask, kernal)
    res = cv2.bitwise_and(img, img, mask=mask)
    rgb2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)


    contours, _ = cv2.findContours(color, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > Area.get():
            # x, y, w, h = cv2.boundingRect(contour)
            # rgb = cv2.rectangle(rgb, (x, y), (x + 50, y + 50), (100, 0, 255), 2)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            co['text'] = 'y= ' + str(int(y)) + '\n' + 'x= ' + str(int(x))
            co.place(x=220, y=690)
            center = (int(x), int(y))
            rgb = cv2.circle(rgb, center, 10, (0, 200, 10), 2)
            if act.get() >= 300: #to switch on the serial
                toSerial(img,x, y)

    to_pil2(rgb, label1, 10, 160)
    to_pil(rgb2, label2, 350, 160, 200, 160)
    to_pil(mask, label3, 350, 340, 200, 160)
    win.after(20, select_img)


select_img()
win.mainloop()
