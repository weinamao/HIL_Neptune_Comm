# Create by Weina Mao on 04/15/2020

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),1333))

msg=s.recv(1024)
print(msg.decode("utf-8"))