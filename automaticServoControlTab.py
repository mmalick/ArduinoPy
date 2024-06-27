from tkinter import Frame, Image, IntVar, Label
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
from state import State
from serial import Serial
from cv2 import VideoCapture
from RangeSlider import RangeSliderH

def hsv(arr):
    arr[0] = round(arr[0] * 255.0 / 360)
    arr[1] = round(arr[1] * 255.0 / 100)
    arr[2] = round(arr[2] * 255.0 / 100)
    return arr

class AutomaticServoControlTab:
    delay = 200
    last_pos = 0
    can_follow = True
    name = 'Automatyczne sterowanie servo'

    def __init__(self, tab_control, ser: Serial, cap: VideoCapture, state: State):
        self.ser = ser
        self.cap = cap
        self.state = state

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

        self.label = Label(self.tab)
        self.label.grid(column=0, row=1)

        tab_control.after(self.delay, self.update)

    def follow_image(self):
        frame = cv.imread("left.png")

        if not self.can_follow:
            return

        lower = hsv(np.array([self.minHue.get(), self.minSaturation.get(), self.minValue.get()]))
        upper = hsv(np.array([self.maxHue.get(), self.maxSaturation.get(), self.maxValue.get()]))

        mask = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(mask, lower, upper)

        bbox = cv.boundingRect(mask)

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        if bbox is not None:
            x, y, w, h = bbox
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        mid = x + w / 2
        value = 180 - int(mid / image.shape[1] * 180)

        if value != self.last_pos:
            self.ser.write(value.to_bytes(1))
            self.last_pos = value

        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image = img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

    def turn(self):
        while self.ser.in_waiting != 0:
            try:
                value = float(self.ser.readline())

                if value > 0 and value < 20:
                    self.ser.write(int(0).to_bytes(1))
                    self.can_follow = False
                else:
                    self.can_follow = True
            except:
                pass

    def update(self):
        if self.state.active_tab != self.name:
            self.tab.after(self.delay, self.update)
            return

        self.turn()
        self.follow_image()
        
        self.tab.after(self.delay, self.update)