# this is an example script to put into impsector, it runs 2 stimuli and then saves them.

import lvbt
import os
import imp
import datetime
import time
os.chdir(r"C:\Users\lvbt\Documents\GitHub\2Photon-Automate")
stim = imp.load_source('Stimulus', 'Stimulus.py')

prepFolder = "C:\\Users\\lvbt\\Documents\\Auto Keiv\\"
if not os.path.isdir(prepFolder):
	os.mkdir(prepFolder)

port = stim.Port()

# Setup a white screen.
looming = stim.StimulusParameters()
looming.filename = "80to2algrating4.mat"
looming.savevideo = "1"
looming.externaltrigger = "1"
looming.repeatstim = "0"
looming.framelength = "1"

# Setup a grating
grating = stim.StimulusParameters()
grating.filename = "Grating_2x1000y4000t1v20w.mat"
grating.savevideo = "0"

# setup imspector measurement
m = lvbt.measurement("Measurement 1")

# run a stimulus, export it and save it. (this could be functionalised)
dt = datetime.datetime.now().strftime('%y%m%d%H%M%S')
recordingFolder, basename = stim.generate_recording_folder(prepFolder,dt)
looming.setup(port)
looming.trigger(port)
m.run()
m.export(recordingFolder, basename)
looming.save(port,recordingFolder + basename + "_stimulus.txt",dt = dt)
looming.reset(port)
looming.quit(port)
'''
# run a second stimulus
dt = datetime.datetime.now().strftime('%y%m%d%H%M%S')
recordingDir, basename = stim.generate_recording_folder(prepFolder,dt)
grating.setup()
grating.trigger()
m.run()
m.export(recordingDir, basename)
grating.save(recordingFolder + basename + "_stimulus.txt", dt = dt)
grating.reset()
'''
port.close()