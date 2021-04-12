import numpy as np
from serial import Serial
import sys
from math import ceil
import time
import os

sys.stderr = open('errors.txt', 'w')

comport = 'COM25'
baudrate = 115200

class Port(Serial):
    """
    Serial port to communicate triggering, aspects of the stimulus.
    """
    def __init__(self, comport='COM25', baudrate=115200):
        super(Port,self).__init__(comport, baudrate, timeout=1)
        if(self.isOpen() == False):
            self.open()
            self.flushInput() # flush the buffer.

    def wait_for_trigger(self, params=None):
        self.flushInput()
        Ported = False
        while not Ported:
            dat = self.read()
            if dat == b't':
                Ported = True # is this necessary? may save a couple us by removing.
              
    def sendover(self, message):
        self.write(str.encode(str(message) + "\n"))
class Parameters(object):
    def parse_parameters(self, paramlist):
        for parameter in paramlist:
            parameter = parameter.split()
            paramtype = parameter[0]
            paramvalue = parameter[1:]
            self.parse_parameter(paramtype, paramvalue)
    def parse_parameter(self, ptype, pvalue):
        if ptype in self.__dict__.keys():
            self.__setattr__(ptype, parse(pvalue))
            #sys.stdout.write(ptype + ": " + str(parse(pvalue)) + "\n")
            #sys.stdout.flush()
        else:
            raise Exception("No attribute named: %s", ptype)
    def save(self, fname):
        with open(fname, 'w') as f:
            f.write('\n'.join(["parameters.%s = %s" % (k,v) for k,v in self.__dict__.items()]))
class StimulusParameters(Parameters):
    def __init__(self):

        self.message = None
        self.adaptionduration = "0"
        self.xpos = "451"
        self.ypos = "519"
        self.xscale = "1"
        self.yscale = "600"
        self.angle = "0"
        self.framelength = "3"
        self.whitebackground = "0"
        self.inversecolor = "0"
        self.externaltrigger = "1"
        self.savevideo = "1"
        self.repeatstim = "1"
        self.filename = "whitescreen.mat"

    def quit(self, port):
        port.write(b'Q\n')

    def save(self, port, filename, dt = None):
        if dt is None:
            port.write(b'S\n')
        else:
            port.sendover('S'+dt)
        with open(filename, 'w') as f:
            f.write('\n'.join(["parameters.%s = %s" % (k,v) for k,v in self.__dict__.items()]))        

    def reset(self, port):
        port.write(b'R\n')

    def change_parameters(self, port):
        port.write(b'C\n')
        port.sendover(self.adaptionduration)
        port.sendover(self.xpos)
        port.sendover(self.ypos)
        port.sendover(self.xscale)
        port.sendover(self.yscale)
        port.sendover(self.angle)
        port.sendover(self.framelength)
        port.sendover(self.whitebackground)
        port.sendover(self.inversecolor)
        port.sendover(self.externaltrigger)
        port.sendover(self.savevideo)
        port.sendover(self.repeatstim)

    def load(self, port):
        port.write(b'L\n')
        port.sendover(self.filename)

    def trigger(self, port):
        port.write(b'T\n')

    def setup(self, port):
        self.load(port)
        self.change_parameters(port)


def generate_recording_folder(prepFolder,basename):
        recordingFolder = prepFolder + "\\" + basename + "\\"
        if not os.path.isdir(recordingFolder):
            os.mkdir(recordingFolder)
        return (recordingFolder, basename)