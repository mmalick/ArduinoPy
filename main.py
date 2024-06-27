import tkinter as tk
from tkinter import ttk
import ctypes
from serial import Serial, SerialException 
import cv2 as cv
from automaticServoControlTab import AutomaticServoControlTab
from detectColorsTab import DetectColorsTab
from detectFacesTab import DetectFacesTab
from detectQRCodesTab import DetectQRCodesTab
from manualServoControlTab import ManualServoControlTab
from readSensorTab import ReadSensorTab
from state import State

state = State()

def on_tab_selected(event):
    selected_tab = event.widget.select()

    tab_text = event.widget.tab(selected_tab, "text")

    state.active_tab = tab_text

ctypes.windll.shcore.SetProcessDpiAwareness(1)

baud_rate = 9600
port = 'COM3'
try:
    ser = Serial(port=port, baudrate=baud_rate, timeout=.1)
except SerialException:
    print('Failed to open serial port')
    ser = None

cap = cv.VideoCapture(0)

root = tk.Tk()
#root.geometry("800x600")
root.geometry("1280x720")
root.title('RobotGUI')

tabControl = ttk.Notebook(root)
tabControl.bind("<<NotebookTabChanged>>", on_tab_selected)

ManualServoControlTab(tabControl, ser, state)
ReadSensorTab(tabControl, ser, state)
DetectQRCodesTab(tabControl, cap, state)
DetectColorsTab(tabControl, cap, state)
DetectFacesTab(tabControl, cap, state)
AutomaticServoControlTab(tabControl, ser, cap, state)

tabControl.pack(expand=1, fill="both")

root.mainloop()
