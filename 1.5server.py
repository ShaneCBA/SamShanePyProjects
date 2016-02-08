#!/usr/bin/env python

import socket
import cPickle

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

def isTouching(player, bullet): 
    for c in [0, 1]:
        if bullet.coords[0][0] < player.coords[c][0] < bullet.coords[1][0] and bullet.coords[0][1] < player.coords[c][1] < bullet.coords[1][1]:
                return True
    return False

retrn = {"players":{},"bullets":{}, "score":{}}
# {name:"name","player": playeraobject, "bullets": (tuple, of, bullets)}
while 1:
    conn, addr = s.accept()
    data = cPickle.loads(conn.recv(BUFFER_SIZE))
    
    if not data:
        continue
        
    retrn["players"][data["name"]]=data["object"]
    retrn["bullets"][data["name"]]=data["bullets"]
    if not (data["name"] in retrn["score"]):
        retrn["score"][data["name"]] = 0
    for keyP, valueP in retrn["players"].iteritems():
        for keyB, valueB in retrn["bullets"].iteritems():
            if isTouching(valueB,valueP):
                    retrn["score"][keyB] += 1
    conn.send(cPickle.dumps(retrn))  # echo
conn.close()