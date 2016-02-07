#!/usr/bin/env python

import socket
import cPickle
import win32api
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
message = {'x':0,'y':10}
count=0
x1,y1 = 0,0
def isTouching(player, bullet): 
    for c in [0, 1]:
        if bullet.coords[0][0] < player.coords[c][0] < bullet.coords[1][0] and bullet.coords[0][1] < player.coords[c][1] < bullet.coords[1][1]:
                return True
    return False
while 1==1:
    MSG = ''
    x, y = win32api.GetCursorPos()
    if x1 != x and y1 != x:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        x1 = x
        y1 = y
        message['x']= x1
        message['y']= y1
        MSG = cPickle.dumps(message)
        s.send(MSG)
        print 'a='
        s.close()
        data = cPickle.loads(s.recv(BUFFER_SIZE))
    time.sleep(0.1)
