General information:
- created by Tomáš Rajchman, David Němec, Eduard Plic, Matyáš Matta and Lucie Kohoutková in early 2023
- if copied please mention authors
- created on the University of West Bohemia in NTIS research centre, thank you so much!

- IMPORTANT: this code may return local errors but all are handled perfectly
- this code does use two threads but their uses are explained clearly and made our whole operation a whole lot easier and reliable
    - please see notes down below for more
- code runs from the if __name__ condition all the way down, NOT from the top to bottom (most is defined as functions)
- all variables are written as to be self-explanatory so we hope it helps
- code might seem complicated but it was tested thoroughly with real ISS data and should work perfectly
- it order to work ALL folders need to be present as they are NOT created, please DO NOT remove them, they contain just readme's to not be empty
- we need at least the shadows.csv, log.txt and main directory to be returned back to Earch!
- we used classes as we all collaborated on the project and it was most sensible for the code to be updated through updating classes (originally we imported them as libraries)
    - hence some classes may seem very small but they are important
- the code depends A LOT on the reliablity of skyfield data and coordinates, please make sure they are as close to current as possible else we get problems with coordinates and their calculations
- all libraries were tested to be present on the AstroPi software by default
- we tested if overheating was an issue and the temperature never went above 350 Kelvins

Files and directories before run:
- chop (temporary stores chopped images)
- main (permanently stores taken whole images)
- model (contains the TFlite model for detections)
- de421.bsp (contains sun data)
- main.py (self-explanatory)
- readme.md (self-explanatory)

Files created during run:
- shadows.csv (file with the project results)
- data.csv (collects SenseHat data, date and temperature)
- log.txt (logs the whole code run)