#!/usr/bin/env python

import time
from printrun.printcore import printcore
from printrun import gcoder
import os
import unicornhathd
import curses
import subprocess

# This presumes the 3D printer is connected as the first USB device and
# that it wants a 115200 baud connection... like our Ender 3 Pro!
print("""connecting to ttyusb0 at 115200 baud""")
global p
p=printcore('/dev/ttyUSB0', 115200) # or p.printcore('COM3',115200) on Windows

print("""sleeping 5 seconds""")
# give it a moment to connect appropriately
time.sleep(5)

#TEST DANCE
print("""zeroing printer""")
#G28 = return to zero point
p.send_now("G28")
#M205 set starting acceleration, default on ender 3 is 20mm/ss
p.send_now("M205 T5")
#track the camera's location because the movement commands are absolute
global camerax
camerax = 0
global cameray
cameray = 0
global cameraz
cameraz = 0

time.sleep(10) #give it time to complete

#coordinates are in tenths of millimeter
print("""sending some other commands now""")

#we should be roughly over the first well now... open the camera!

unicornhathd.brightness(1)
unicornhathd.clear()
unicornhathd.set_all(255, 255, 255)
unicornhathd.show()
#backlight ON

def focuscyka(win):
	global camerax
	global cameray
	global cameraz
	print("I am opening the camera!")
	#-t 0 leaves the window open indefinitely
	#camerapid = os.system("libcamera-hello -t 0 &")
	cameraproc = subprocess.Popen(["libcamera-hello", "-t", "0"])	
	cameraz = 11
	p.send_now('G0 Z{}'.format(cameraz))

	camerax = 12
	p.send_now('G0 X{}'.format(camerax))
	cameray = 39
	p.send_now('G0 Y{}'.format(cameray))
	while True:
		try:
			key = win.getch()

			
			if key == ord('w'):
				cameraz = cameraz + 1
			if key == ord('s'):
				cameraz = cameraz - 1
			if key == ord('a'):
				camerax = camerax + 1
			if key == ord('d'):
				camerax = camerax - 1
			if key == ord('r'):
				cameray = cameray - 1
			if key == ord('f'):
				cameray = cameray + 1
											
			if key == ord('p'):
				os.system('kill {}'.format(cameraproc.pid))
				unicornhathd.off()
				break
			p.send_now('G0 Z{}'.format(cameraz))
			p.send_now('G0 X{}'.format(camerax))
			p.send_now('G0 Y{}'.format(cameray))
			
			win.addstr(" X:")
			win.addstr(str(camerax))
			win.addstr(" Y:")
			win.addstr(str(cameray))
			win.addstr(" Z:")
			win.addstr(str(cameraz))
						
			time.sleep(.5)
		except Exception as e:
			# no input?
			pass



curses.wrapper(focuscyka)			
# done focusing, allegedly
global camerahomex
global camerahomey
global camerahomez
camerahomex = camerax
camerahomey = cameray
camerahomez = cameraz
# now that we know where the bottom left well is, we can start taking pictures

frame = 0

#compensate for our focus spot being the center of the well
#camerax = camerax - 3
#cameray = cameray - 3

xwell = 0
ywell = 0
while ywell < 3:
	xwell = 0
	camerax = camerahomex
	cameray = cameray + 18
	ywell = ywell + 1
	while xwell < 5:
		xwell = xwell + 1
		xframe = 0
		yframe = 0
		#we get signal
		#main screen turn on
		unicornhathd.brightness(1)
		unicornhathd.clear()
		unicornhathd.set_all(255, 255, 255)
		unicornhathd.show()
		
		while yframe < 1:
			yframe = yframe + 1
			xframe = 0
			while xframe < 1:
				xframe = xframe + 1
				print("I am taking a picture of well {}, {} at subcoords {}, {}".format(xwell, ywell, xframe,yframe))
		
				#shutter speed 100ms, gain 80%
				#i dont know microscopy or photograph very well so i am just playing around with these settings really
				#os.system("libcamera-jpeg -o photos/{}.jpg -t 1 --shutter 100000 --gain 0.8".format(frame))
				os.system("libcamera-still -e bmp -o ./photos/{}_{}_{}_{}.bmp -t 1 --shutter 100000 --gain 0.8 --immediate".format(xwell,ywell,xframe,yframe))
				time.sleep(1)
				
				#p.send_now('G0 Y{}'.format(cameray + yframe))
				#p.send_now('G0 X{}'.format(camerax + xframe))
				
				#transit time between coordinates
				time.sleep(2)
		
		unicornhathd.off()
		#move to the next wellthe wells are i think 18mm apart
		camerax = camerax + 18
		
		#move the head
		#p.send_now('G0 Z{}'.format(cameraz))
		p.send_now('G0 Y{}'.format(cameray))
		p.send_now('G0 X{}'.format(camerax))
		
		#transit time between wells
		time.sleep(4)




#p.send_now("G28") #back home

#p.disconnect()
