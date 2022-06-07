import numpy as np 
import cv2 
import pickle 
import tkinter as tk
# from tkinter import *
import pickle 

name = ""
ids = 1

ril = 0

                    
                   
    
# make a login page GUI using tkinter
class Login(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.frames = {}
    
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        for F in (LoginPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(LoginPage)
        
    
    def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()


class LoginPage(tk.Frame):
    name = "Selamat Datang"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Selamat Datang di Program Login Face Recognition", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)


        button = tk.Button(self, text="login", command=lambda: self.faceRecognition(parent, controller))
        button.pack()

        
    def faceRecognition(self, parent, controller):
        
        face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("trainer.yml")

        labels = {"person_name": 1}
        with open("labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            labels = {v:k for k,v in og_labels.items()}

        cap = cv2.VideoCapture(0)
    
        while True:
            try:    # Capture frame-by-frame
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                for (x, y, w, h) in faces:
                    # print(x,y,w,h)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]
                    id_, conf = recognizer.predict(roi_gray) 
                    if conf >= 45 and conf <= 85:
                        print(id_)
                        print(labels[id_])
                        LoginPage.name = "halo"
                        page = PageOne(parent, controller)
                        controller.show_frame(PageOne)
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                    else:
                        print("unknown")


                    color = (255, 0, 0) #BGR and not RGB
                    stroke = 2
                    end_cord_x = x + w
                    end_cord_y = y + h
                    cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
                # Display the resulting frame
                cv2.imshow('frame', frame)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            except:
                break
            #when everything done, release the Capture
        cap.release()
        cv2.destroyAllWindows()
        
    
    

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print("Hello world")
    
        label = tk.Label(self, text=LoginPage.name, font=("Helvetica", 18))
        label.pack(pady=10, padx=10)
   





window = Login()
window.title("Login Page")
window.mainloop()
