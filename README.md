# Patch4Butler

This repository contains the post processing script to be called by Slic3r after gcode was generated. The script will patch the gcode file by adding necessary gcode commands used to control butler on MMU2 unit


To use a Python post-processing script with Windows, you'll need to adjust the paths like this:

C:\Program! Files! (x86)\Python37-32\python.exe c:\dev\SCPP\Patch4MmuButler.py

Notes: 
- Set the correct path to python. On windwos sue cmd-> where python to find out the correct installation path
- Important: A ! needs to be set before all white-spaces! Make sure you adjust the path to your script as well.

