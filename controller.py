#-*- coding: utf-8 -*-
# coding: utf8
from bibliopixel.led import *
from bibliopixel.animation import StripChannelTest
from bibliopixel.drivers.LPD8806 import *
from BiblioPixelAnimations.strip import Rainbows
from BiblioPixelAnimations.strip import WhiteTwinkle
from BiblioPixelAnimations.strip import FireFlies
from time import sleep


def init():

    global ledfarbefile
    ledfarbefile= open("led.txt" , "r")
    global ledfarbe
    ledfarbe = ledfarbefile.read()
    ledfarbefile.close()

    helligkeitfile = open("helligkeit.txt" , "r")
    global helligkeitraw
    helligkeitraw = helligkeitfile.read()
    helligkeitfile.close()

    animationfile = open("animation.txt" , "r+")
    global animation
    animation = animationfile.read()
    animationfile.close()

    try:
       global helligkeit
       helligkeit = int (helligkeitraw)
    except Exception as e:
       pass

    global masterhelligkeit
    masterhelligkeit = (( helligkeit * 255) // 100)
    global driver
    driver = DriverLPD8806(52)
    global led
    led = LEDStrip(driver, masterBrightness=masterhelligkeit)
    global anim
    anim = None


def readcolor():
     ledfarbefile = open("led.txt" , "r")
     ledfarbe = ledfarbefile.read()
     ledfarbefile.close()
     return ledfarbe


def readanimation():
    animationfile = open("animation.txt", "r")
    animation = animationfile.read()
    animationfile.close()
    return animation


def writeanimation(string):
    animationfile = open("animation.txt", "w")
    animationfile.seek(0)
    animationfile.truncate()
    animationfile.write(string)
    animationfile.close()


def stat(s):
    if s == "an":
        farb(readcolor())
    else:
        stoper()
        led.all_off()
        led.update()


def farb (f):
     print f
     turnOff()
     if readanimation() != "stop":
        stoper()
        writeanimation("stop")
        led.update()
     if f == "weiss" or f == "weiß":
        led.fillRGB(255,255,255)
     elif f == "blau":
        led.fillRGB(255,0,0)
     elif f == "rot":
        led.fillRGB(0,255,0)
     elif f == "gelb":
        led.fillRGB(0,255,255)
     elif f == "gruen":
         led.fillRGB(0, 0, 255)
     elif f == "lernen":
         led.fillRGB(190, 230, 224)
     elif f == "lesen":
         led.fillRGB(175, 220, 215)
     led.update()


def stoper():
    global anim
    if anim is not None:
        anim.stopThread()


def anima (a):
    stoper()
    global anim
    if a == "ambient":
        anim = Rainbows.RainbowCycle(led)
        print anim.step
        anim.run(threaded = True)
    elif a == "funkeln":
        print "funkeln"
        anim = WhiteTwinkle.WhiteTwinkle(led)
        anim.run(threaded = True)
    elif a == "firefly":
        anim = FireFlies.FireFlies(led,colors)
        anim.run(threaded = True)
    elif a == "stop":
         farb(readcolor())


def turnOff():
    led.all_off()
    led.update()


def hell (he):
   global masterhelligkeit
   masterhelligkeit = ((255 * he) // 100)
   global led
   led = LEDStrip(driver, masterBrightness=masterhelligkeit)

   animation = readanimation()
   if animation == "stop":
       init()
       farb(readcolor())
   else:
        anima(animation)

