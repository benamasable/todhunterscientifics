#!/usr/bin/env python

import time

import os
import unicornhathd

print("""Sowbug Camera Test Captures

This script will first turn on the Unicorn HD hat to full brightness.
It will then call the libcamera-jpeg function once every second to
take a picture.


Press Ctrl+C to exit!

""")

unicornhathd.brightness(1)
unicornhathd.clear()
unicornhathd.set_all(255, 255, 255)
unicornhathd.show()
#FULL POWER

#this will also be the filenames
frame = 0

#delay between frames, in seconds
delaytime = 5

t_start = time.time()
t_nextframe = t_start + 1

try:
	#numer of pictures we will take
	while frame < 1:
	# BING BONG time to take a picture
		if time.time() >= t_nextframe:
			t_nextframe += delaytime
			frame += 1
			print("I am taking picture number {}".format(frame))
			#shutter speed 100ms, gain 80%
			#i dont know microscopy or photograph very well so i am just playing around with these settings really
			#os.system("libcamera-jpeg -o photos/{}.jpg -t 1 --shutter 100000 --gain 0.8".format(frame))
			os.system("libcamera-still -e bmp -o ./photos/{}.bmp -t 1 --shutter 100000 --gain 0.8 --immediate".format(frame))
	unicornhathd.off()
	
except KeyboardInterrupt:
#turn off the hat, for the sake of your eyeballs
    unicornhathd.off()

