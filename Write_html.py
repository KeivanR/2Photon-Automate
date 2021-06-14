import Experiment_parameters as exp
import os
def update(text,size,path = exp.path_server):
    os.system('python C:\\Users\\lvbt\\Documents\\GitHub\\2Photon-Automate\\Screenshot.py')
    f = open(path+'index.html','w')
    message = """<html>
    <head></head>
    <body> <p style='font-size:"""+str(size)+"""px'>""" + text + """</p> </body>
    <img src='screenshot.png' alt="Current screen" width = '1000' height = '600'>  
    </html>"""

    f.write(message)
    f.close()
#update('lol',33)