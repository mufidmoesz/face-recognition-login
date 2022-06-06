import numpy as np 
import cv2 
import pickle 
import tkinter as tk
from tkinter import *
import pickle 

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")
labels = {"person_name": 1}
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}


def faceRecognition():
    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        global name

        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            id_, conf = recognizer.predict(roi_gray)
            if conf >= 45 and conf <= 85:
                print(id_)
                print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                Login.self.show_frame(PageOne)
                break
            else:
                print("Unknown")
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = "Unknown"
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
# make a login page GUI using tkinter
class Login(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.pack(side="top", fill="both", expand=True)
        
        self.show_frame(LoginPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, controller)
        label = tk.Label(self, text="Selamat Datang di Program Login Face Recognition", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="login", command=faceRecognition)
        button.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, controller)
        label = tk.Label(self, text=f"Selamat Datang{name}", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

root = Login()
root.mainloop()

        

# root.title("Login Page")

# root.geometry("600x400")
# root.resizable(False, False)
# root.configure(background="black")

# welcome = tk.Label(root, text="Selamat Datang di Program Login Face Recognition", font=("Helvetica", 18), bg="black", fg="white")
# welcome.place()

# root.mainloop()