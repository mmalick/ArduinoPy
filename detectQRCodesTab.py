from tkinter import Frame, Label

from cv2 import VideoCapture
import cv2
from state import State
from PIL import Image, ImageTk

class DetectQRCodesTab:
    def __init__(self, tab_control, cap: VideoCapture, state: State):
        self.cap = cap
        self.state = state
        self.name = 'Wykrywanie kodów QR'
        self.delay = 100

        self.tab = Frame(tab_control)

        tab_control.add(self.tab, text=self.name)

        self.label = Label(self.tab)
        self.label.pack()

        self.qrlabel = Label(self.tab)
        self.qrlabel.pack()

        self.label.after(self.delay, self.update)
        
    def update(self):
        if self.state.active_tab != self.name:
            self.label.after(self.delay, self.update)
            return

        ret, frame = self.cap.read()

        if not ret:
            self.label.after(self.delay, self.update)
            return

        frame = cv2.cvtColor(frame ,cv2.COLOR_BGR2RGB)

        qcd = cv2.QRCodeDetector()

        retval, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)

        if retval:
            frame = cv2.polylines(frame, points.astype(int), True, (0, 255, 0), 3)

            for s, p in zip(decoded_info, points):
                frame = cv2.putText(frame, s, p[0].astype(int), cv2.QT_FONT_NORMAL, 1, (255, 0, 0), 1, cv2.LINE_AA)

            self.qrlabel.config(text=decoded_info)

        img = Image.fromarray(frame)

        imgtk = ImageTk.PhotoImage(image = img)

        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        self.label.after(self.delay, self.update)
