@echo off 

adb shell screencap -p /storage/emulated/0/DCIM/screenshot.png 

adb pull "/storage/emulated/0/DCIM/screenshot.png" ".\Report" 

adb shell rm "/storage/emulated/0/DCIM/screenshot.png" 
