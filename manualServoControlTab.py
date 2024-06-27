from tkinter import Button, Frame
from state import State
from serial import Serial

class ManualServoControlTab:
    name = 'Manualne sterowanie servo'

    def __init__(self, tab_control, ser: Serial, state: State):
        self.ser = ser
        self.state = state

        self.tab = Frame(tab_control)

        tab_control.add(self.tab, text=self.name)

        leftButton = Button(self.tab, text="Left", padx=30, pady=10, command=self.moveLeft)
        leftButton.pack(side='left', expand=True)

        rightButton = Button(self.tab, text="Right", padx=30, pady=10, command=self.moveRight)
        rightButton.pack(side='right', expand=True)

    def moveLeft(self):
        try:
            if self.ser is not None:
                #self.ser.write(bytes('L', "ASCII"))
                self.ser.write(int(0).to_bytes(1))
        except:
            print("Turn left failed")

    def moveRight(self):
        try:
            if self.ser is not None:
                #self.ser.write(bytes('R', "ASCII"))
                self.ser.write(int(180).to_bytes(1))
        except:
            print("Turn right failed")
