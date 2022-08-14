import socket
from substitution_functions import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.0.3"
print("\nQuestion 2 - Client\n" + host)
port = 10000
s.connect((host, port))

texts = ["zoo", "xray", "rellis", "college station", "csci458"]

# let the server know what encryption we're using for the remainder
# of this connection for the sake of showing on the homework
s.send("CAESAR".encode())
msg = s.recv(1024)
for text in texts:
    message = encryptCaesar(text)
    s.send(message.encode())

    msg = s.recv(1024)
    msg = decryptCaesar(msg.decode())
    print("received: " + msg)
s.close()
print()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send("ROT13".encode())
msg = s.recv(1024)
for text in texts:
    message = ROT13(text)
    s.send(message.encode())

    msg = s.recv(1024)
    msg = ROT13(msg.decode())
    print("received: " + msg)
s.close()
print()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send("C3".encode())
msg = s.recv(1024)
for text in texts:
    message = encryptC3(text)
    s.send(message.encode())

    msg = s.recv(1024)
    msg = decryptC3(msg.decode())
    print("received: " + msg)
s.close()
