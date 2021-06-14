import lvbt
import os
import imp
import datetime
import time
import numpy as np
import random
import sys
os.chdir(r"C:\Users\lvbt\Documents\GitHub\2Photon-Automate")
stim = imp.load_source('Stimulus', 'Stimulus.py')
exp = imp.load_source('Experiment_parameters', 'Experiment_parameters.py')
gen = imp.load_source('Generate', 'Generate.py')
listim = imp.load_source('List_stimuli', 'List_stimuli.py')
wh = imp.load_source('Write_html', 'Write_html.py')

prepFolder = exp.prepFolder
if not os.path.isdir(prepFolder):
	os.mkdir(prepFolder)

port = stim.Port()
try:
    # setup imspector measurement
    m = lvbt.measurement("Measurement 1")
    # run a stimulus, export it and save it. (this could be functionalised)
    stimuli = []
    stimuli += listim.rf_bars(repeat = 2)
    #stimuli += listim.repeat_stim('flash1200.mat',0,10)
    #stimuli += listim.dyna_gratings(speed=[1,2,3],noise=True,reverse=True)
    #stimuli += listim.one_stim('300to1blink1.mat',0)
    #stimuli2 = listim.repeat_stim('5to100algrating2.mat',0,40)+listim.repeat_stim('5to100algrating2.mat',180,40)
    
    stimuli2 = listim.algratings([1,2,3],[5,10,15,20,40,60,100],10)
    random.shuffle(stimuli2)
    stimuli += stimuli2
    print(listim.names(stimuli))
    inter_time = 12
    duration = int((700/15.3+inter_time)*len(listim.names(stimuli)))-inter_time
    print('Duration: ',str(datetime.timedelta(seconds=duration)))
    i = 0
    for stimulus in stimuli:
        t0 = time.time()
        percentage = int(100*i/len(stimuli))
        dt = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        recordingFolder, basename = stim.generate_recording_folder(prepFolder,dt)
        stimulus.setup(port)
        stimulus.trigger(port)
        start = time.time()
        m.run()
        if time.time()-start<exp.rec_time_limit:
            break
        m.export(recordingFolder, basename)
        stimulus.save(port,recordingFolder + basename + "_stimulus.txt",dt = dt)
        i += 1
        duration = int((time.time()-t0)*len(stimuli))
        wh.update(str(percentage)+'%<br>'+stimulus.filename+'<br>('+str(datetime.timedelta(seconds=duration*(100-percentage)/100))+' left)',size = 70)
    stimuli[-1].reset(port)
    stimuli[-1].quit(port)
    wh.update('Experiment finished!',size = 150)

    port.close()

except:
    stimuli[-1].reset(port)
    stimuli[-1].quit(port)
    port.close()
    wh.update("Oops!"+str(sys.exc_info()[0])
+"occurred.",size = 150)