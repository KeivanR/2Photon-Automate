import Experiment_parameters as exp
import mss
#f = open('C:\\Users\\lvbt\\Documents\\index.html','w')
with mss.mss() as sct:
	filename = sct.shot(output=exp.path_server+'screenshot.png')
    
