from cmath import pi
import math 
import geopy
import geopy.distance
import requests
import selenium
from bs4 import BeautifulSoup #pip install beautifulsoup4
from os import link
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from bs4 import BeautifulSoup #pip install beautifulsoup4
import tkinter as tk
from tkinter import ttk
import csv
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import csv
from datetime import datetime
import requests
from selenium.webdriver.chrome.service import Service

fieldOfView = 50
earthCircumference = 40075017

relativeDistance = input("Input the pixel distance between cloud and shade (px): ")

def distance(fieldOfView, distanceinpixels):
    fieldOfViewRadians = fieldOfView*(pi/180)
    distanceinmeters = int(distanceinpixels)*142
    return distanceinmeters

def coordinates(relativeCoordinates, xcorrectionPixels, ycorrectionPixels):
    global absoluteCoordinates
    relativeCoordinatesGeoPy = geopy.Point(relativeCoordinates)

    xcorrectionKilometers = distance(fieldOfView, xcorrectionPixels)
    ycorrectionKilometers = distance(fieldOfView, ycorrectionPixels)

    xcorrectionMeta = geopy.distance.geodesic(kilometers = xcorrectionKilometers)
    ycorrectionMeta = geopy.distance.geodesic(kilometers = ycorrectionKilometers)
    
    xcorrectionDegrees = xcorrectionMeta.destination(point=relativeCoordinatesGeoPy, bearing=0)
    ycorrectionDegrees = ycorrectionMeta.destination(point=relativeCoordinatesGeoPy, bearing=180)

    print(xcorrectionDegrees, ycorrectionDegrees)

def link(relativeLatitude, relativeLongitude, date, time):
    linkstring = 'https://suncalc.org/#/'+relativeLatitude+","+relativeLongitude+",17"+"/"+date+"/"+time+"/324.0/2"
    return linkstring

absoluteDistance = distance(fieldOfView, relativeDistance)

relativeLatitude = input("Input the photo latitude coordinate (xx.x format): ")
relativeLongitude = input("Input the photo longitude coordinate (xx.x format): ")
date = input("Input photo date (yyyy.mm.dd): ")
time = input("Input photo time (hh:mm:ss): ")

linkstring = link(relativeLatitude, relativeLongitude, date, time)
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--allow-mixed-content")
executablePathWebDriverChrome = '.\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=executablePathWebDriverChrome)
driver.get(linkstring)
altitudeXPath = '//*[@id="sunhoehe"]'
altitude = driver.find_element("xpath", altitudeXPath).text

print(altitude, absoluteDistance)

altitude = altitude[0:-1]
altitude = math.radians(float(altitude))
cloudheight = math.tan(altitude)*absoluteDistance

print(cloudheight)
wait = input("wait")