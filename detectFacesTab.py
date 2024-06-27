from tkinter import DoubleVar, Frame, Label, Scale
from cv2 import VideoCapture
import cv2 as cv
from PIL import Image, ImageTk

from state import State

class DetectFacesTab:
    def __init__(self, tab_control, cap: VideoCapture, state: State):
        self.cap = cap
        self.state = state
        self.name = 'Wykrywanie twarzy'
        self.delay = 20

        self.tab = Frame(tab_control)

        tab_control.add(self.tab, text=self.name)

        self.scaleFactor = DoubleVar(value=1.1)

        scale = Scale(self.tab, from_=1.01, to=2.0, resolution=0.01, length=300, variable=self.scaleFactor, orient='horizontal')
        scale.pack()

        self.label = Label(self.tab)
        self.label.pack()

        self.label.after(self.delay, self.update)

    def update(self):
        if self.state.active_tab != self.name:
            self.label.after(self.delay, self.update)
            return

        ret, frame = self.cap.read()

        if not ret:
            self.label.after(self.delay, self.update)
            return

        face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, self.scaleFactor.get(), 4)

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        for (x, y, w, h) in faces:
            cv.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        imgtk = ImageTk.PhotoImage(image = Image.fromarray(image))

        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        self.label.after(self.delay, self.update)