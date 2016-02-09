#!/usr/bin/env python
import socket as sckt
import cPickle
import select
import sys 

host = '127.0.0.1'
port = 5000
BUFFER_SIZE = 99999
backlog = 2

server = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
server.setsockopt(sckt.SOL_SOCKET, sckt.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(backlog)

input = [server,sys.stdin]
running = 1

playerCount = 0

while running:
    inputready,outputready,exceptready = select.select(input,[],[])
    
    for s in inputready:
        if s == server:
            if playerCount < backlog:
                client, address = server.accept()
                input.append(client)
                playerCount += 1
        elif s == sys.stdin:
            read = sys.stdin.readline()
            if read.lower() == 'stop':
                running = 0
        else:
            data = cPickle.loads(s.recv(BUFFER_SIZE))
            if data:
                s.send(data)
            else:
                s.close()
                input.remove(s)    
    
server.close()