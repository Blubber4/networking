import socket
import threading

from substitution_functions import *

# adding a timeout for clients would be a good idea
def handleClient(csocket, address):
    print("Got a connection from " + str(address))
    mode = ""
    while True:
        data = csocket.recv(1024)
        if not data:
            break

        # first message received in a communication session will decide encryption mode for the rest of the session
        # no mode specified in first message = no encryption
        message = data.decode()
        if message == "CAESAR" or message == "ROT13" or message == "C3":
            mode = message
            print("mode:", mode)
            csocket.send(mode.encode())
            continue

        msg = ""
        if mode == "CAESAR":
            message = decryptCaesar(message)
            msg = encryptCaesar(message)
        elif mode == "ROT13":
            message = ROT13(message)
            msg = ROT13(message)
        elif mode == "C3":
            message = decryptC3(message)
            msg = encryptC3(message)
        print("received: " + data.decode())
        print("decrypted: " + message)
        csocket.send(msg.encode())

    print()
    csocket.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.0.3"
port = 10000
serversocket.bind((host, port))
serversocket.listen()

print('\nQuestion 2 - Server\nwaiting for a connection on port ' + str(port))
while True:
    clientsocket, addr = serversocket.accept()
    # handling client connections in their own thread - concurrent sessions should work??
    clientthread = threading.Thread(target=handleClient, args=(clientsocket, addr))
    clientthread.start()






