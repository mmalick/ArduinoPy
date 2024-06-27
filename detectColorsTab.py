from tkinter import Frame, Image, IntVar, Label
from cv2 import VideoCapture
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np
from state import State
from RangeSlider import RangeSliderH

def hsv(arr):
    arr[0] = round(arr[0] * 255.0 / 360)
    arr[1] = round(arr[1] * 255.0 / 100)
    arr[2] = round(arr[2] * 255.0 / 100)
    return arr

class DetectColorsTab:
    def __init__(self, tab_control, cap: VideoCapture, state: State):
        self.cap = cap
        self.state = state
        self.name = 'Wykrywanie kolorów'
        self.delay = 20

        self.tab = Frame(tab_control)

        tab_control.add(self.tab, text=self.name)

        self.row = Frame(self.tab)
        self.row.grid(row=0, column=0, columnspan=3)

        hueLabel = Label(self.row, text="H")
        hueLabel.pack(side='left')

        self.minHue = IntVar(value = 0)
        self.maxHue = IntVar(value = 360)
        hueSlider = RangeSliderH(self.row, [self.minHue, self.maxHue], min_val=0, max_val=360, padX=18, Height=64, step_size=1, digit_precision='.0f')
        hueSlider.pack(side='left')

        saturationLabel = Label(self.row, text="S")
        saturationLabel.pack(side='left')

        self.minSaturation = IntVar(value = 0)
        self.maxSaturation = IntVar(value = 100)
        saturationSlider = RangeSliderH(self.row, [self.minSaturation, self.maxSaturation], min_val=0, max_val=100, padX=18, Height=64, step_size=1, digit_precision='.0f')
        saturationSlider.pack(side='left')

        valueLabel = Label(self.row, text="V")
        valueLabel.pack(side='left')

        self.minValue = IntVar(value = 0)
        self.maxValue = IntVar(value = 100)
        valueSlider = RangeSliderH(self.row, [self.minValue, self.maxValue], min_val=0, max_val=100, padX=18, Height=64, step_size=1, digit_precision='.0f')
        valueSlider.pack(side='left')

        self.left = Label(self.tab)
        self.left.grid(column=0, row=1)

        self.middle = Label(self.tab)
        self.middle.grid(column=1, row=1)

        self.right = Label(self.tab)
        self.right.grid(column=2, row=1)

        self.tab.after(self.delay, self.update)
        
    def update(self):
        if self.state.active_tab != self.name:
            self.tab.after(self.delay, self.update)
            return

        ret, frame = self.cap.read()

        if not ret:
            self.tab.after(self.delay, self.update)
            return

        lower = hsv(np.array([self.minHue.get(), self.minSaturation.get(), self.minValue.get()]))
        upper = hsv(np.array([self.maxHue.get(), self.maxSaturation.get(), self.maxValue.get()]))

        mask = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(mask, lower, upper)

        #contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        bbox = cv.boundingRect(mask)

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        if bbox is not None:
            x, y, w, h = bbox
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #cv.drawContours(image, contours, -1, (255, 0, 0), 3)
        #if len(contours) >= 4:
        #    cnt = contours[4]
        #    cv.drawContours(image, [cnt], 0, (0,255,0), 3)

        maskedImage = cv.bitwise_and(image, image, mask=mask)

        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image = img)
        self.left.imgtk = imgtk
        self.left.configure(image=imgtk)

        img = Image.fromarray(maskedImage)
        imgtk = ImageTk.PhotoImage(image = img)
        self.middle.imgtk = imgtk
        self.middle.configure(image=imgtk)

        img = Image.fromarray(mask)
        imgtk = ImageTk.PhotoImage(image = img)
        self.right.imgtk = imgtk
        self.right.configure(image=imgtk)

        self.tab.after(self.delay, self.update)