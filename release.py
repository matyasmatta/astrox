import threading
import time
from time import sleep
import cv2
import numpy as np
from numpy import average 
import statistics
from PIL import Image, ImageStat
from pycoral.adapters import common, detect
from pycoral.utils.edgetpu import make_interpreter
from skyfield import api
from skyfield.api import load
import csv
from csv import writer
from datetime import timedelta, datetime
from pathlib import Path
from exif import Image as exify
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

def openfile():
    name = fd.askopenfilename()
    return name[19:]
class MyApp(tk.Frame):
    def file_openerfunction(self):
        self.filename = openfile()
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.window = Tk()
        mb = Menu(self.window)

        self.window.title("Digital Atmospheric Visual Inspection and Detection")
        width = 720
        height = 400
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.window.resizable(0, 0)

        self.menu_bar = Menu(mb, tearoff=0)  
        self.menu_bar.add_command(label="File Analysis")  
        self.menu_bar.add_command(label="Batch Analysis", command=self.file_openerfunction)
        self.menu_bar.add_command(label="Save")  
        self.menu_bar.add_command(label="Save as...")  
        self.menu_bar.add_command(label="Close")  

        self.menu_bar.add_separator()  
        self.window.config(menu=mb)

        self.label = tk.Label(text="All credit @matyasmatta in April 2023")
        self.label.pack()

        self.menu_bar.add_command(label="Exit Program", command=self.window.quit)  

        mb.add_cascade(label="File", menu=self.menu_bar)


app = MyApp()
app.mainloop()

counter = 0
try:
    os.mkdir("./output")
except:
    pass
for images in os.listdir("./batch/"):
    try:
        counter += 1
        name = os.listdir("./batch/")[counter]
        name = name[:-3]
        path = "./output/" + name
        os.mkdir(path)
    except:
        break