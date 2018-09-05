# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 10:46:30 2018

@author: mimo
"""
from ptpy import PTPy
from ptpy.transports.ip import IPTransport

from ptpy.extensions.fulldome import Fulldome

from time import sleep
from datetime import datetime

print('Starting script at ' + str(datetime.now()))

camera = PTPy(transport=IPTransport, device='192.168.1.1', knowledge=False,
              extension=Fulldome)

recordingTime = 10

with camera.session():
    print('Top level session:')
    print(camera.session_id)
    
    print('Syncinc Time.')
    camera.SyncTime()
    print('Recording for %d seconds.'%recordingTime)
    camera.StartRecording()
    for seconds in range(recordingTime):
        print("%d.."%seconds)
        sleep(1)
    camera.StopRecording()
    print('Finished recording.')
