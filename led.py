#-*- coding: utf-8 -*-

from flask import Flask
from flask_ask import Ask, statement, convert_errors, audio
import logging
import os
from pytube import YouTube
import pafy

import controller

controller.init()

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('licht', mapping={'status': 'status', 'farbe': 'farbe', 'helligkeit': 'helligkeit', 'animation': 'animation' })
def led(status,farbe, helligkeit, animation):

    if status is not None:
        f = open("/home/pi/LED/status.txt" , "w")
        f.seek(0)
        f.truncate()
        f.write(status)
        f.close()
        controller.stat(status)
        return statement('LEDs {} '.format(status))

    elif farbe is not None:
        farbe = unicode.encode(farbe, 'UTF-8')
        farbe = farbe.lower()
        f = open("/home/pi/LED/led.txt", "w")
        f.seek(0)
        f.truncate()
        f.write(farbe)
        f.close()
        controller.farb(farbe)
        return statement('LEDs {} '.format(farbe))

    elif helligkeit is not None:
        try:
            pinNum = int(helligkeit)

        except Exception as e:
            return statement('Helligkeit ist keine Zahl.')
        f = open("/home/pi/LED/helligkeit.txt", "w")
        f.seek(0)
        f.truncate()
        f.write(helligkeit)
        f.close()
        controller.hell(pinNum)
        return statement('LEDs {} '.format(helligkeit))

    elif animation is not None:
        f = open("/home/pi/LED/animation.txt", "w")
        f.seek(0)
        f.truncate()
        f.write(animation)
        f.close()
        controller.anima(animation)
        return statement('LEDs {} '.format(animation))

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port)

