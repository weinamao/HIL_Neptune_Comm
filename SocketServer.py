import socket
from EngineDemo import *
from LegacyPython import *

port = 1333
maxConnection = 999
IP = socket.gethostname()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('', port))
s.listen(maxConnection)
print('Server Started at '+IP+' on port '+str(port)+'.')


while True:
    (clientsocket, address) = s.accept()
    print(f"Connection from {address} has been established!")
    # engine_demo_basic(BooleanValue(True), DoubleValue(2500))
    mix_legacy_and_rtseq_run()
    print('Finished non-deterministic')
    clientsocket.send(bytes("Welcome to the server!",'utf-8'))