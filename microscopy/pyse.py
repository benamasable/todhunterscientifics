#!/usr/bin/env python

from serial import Serial
import time

class HDTerm(Serial):

    def __init__(self, *args, **kwargs):
        #ensure that a reasonable timeout is set
        timeout = kwargs.get('timeout',0.1)
        if timeout < 0.01: timeout = 0.1

        kwargs['baudrate'] = 115200
        kwargs['port'] = '/dev/ttyUSB0'
        #kwargs['parity'] = Serial.PARITY_ODD
        #stopbits=serial.STOPBITS_ONE,
        #bytesize=serial.EIGHTBITS

        kwargs['timeout'] = timeout
        Serial.__init__(self, *args, **kwargs)
        self.buf = '' 

        if self.isOpen():
            self.close()
        self.open()

        self.isOpen()


    def rd(self):
        time.sleep(1)
        out = ''

        while self.inWaiting() > 0:

            out += ser.read(40)

        print('  <- ', (out))

    def wt(self, data):
        ed = data.encode()
        print('  -> ', (ed))
        self.write(ed)


    def inp(self):
        st = input('> ')

        self.wt(st)
        self.rd()
        self.inp()

if __name__ == '__main__':
    hdterm = HDTerm()
    hdterm.inp()
