from tkinter import Frame
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from state import State
from serial import Serial

class ReadSensorTab:
    name = "Odczyt danych z sensora"
    delay = 100
    maxLength = 100

    def __init__(self, tab_control, ser: Serial, state: State):
        self.ser = ser
        self.state = state

        self.data = self.maxLength * [0]
        
        self.tab = Frame(tab_control)

        tab_control.add(self.tab, text=self.name)

        fig = Figure(figsize = (5, 5)) 
    
        self.plot1 = fig.add_subplot(111)
    
        self.canvas = FigureCanvasTkAgg(fig, master = self.tab)   
        self.canvas.draw() 
        self.canvas.get_tk_widget().pack() 
    
        toolbar = NavigationToolbar2(self.canvas) 
        toolbar.update() 
    
        self.canvas.get_tk_widget().pack() 

        if self.ser is not None:
            self.tab.after(self.delay, self.update)

    def update(self):
        if self.state.active_tab != self.name:
            self.tab.after(self.delay, self.update)
            return
        
        while self.ser.in_waiting != 0:
            try:
                value = float(self.ser.readline())
                value = min(value, 100)
                self.data.append(value)
                self.data.pop(0)
            except:
                pass

        self.plot1.cla()
        self.plot1.plot(self.data)

        self.canvas.draw()

        self.tab.after(self.delay, self.update)
