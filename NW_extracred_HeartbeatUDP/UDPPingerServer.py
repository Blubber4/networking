# UDPPingerServer.py

# Standard python print() has a multi-step process where it:
# 1. pushes the given string to a buffer
# 2. pushes a newline character to the buffer
# 3. displays the buffer
# This was causing issues with inconsistent newline character positions when trying to print while something was also
# being printed in threaded parts, so sys.stdout.write() needs to be used instead at all times.

# I think there might be issues with the thread locking here for multiple clients, for example with removing clients
# in updateTimeout(), so this may or may not be immediately usable code if there are multiple concurrent clients.
# Works fine with only one client sending packets at a time though.
import random
import socket
import sys
import threading
import time

class ActiveClientList(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.clients = [] # list of three values: address, last sequence number received, last time packet was received
        self.timeout = 30.0

    def getClient(self, addr):
        self.lock.acquire()
        for client in self.clients:
            if client[0] == addr:
                self.lock.release()
                return client
        self.lock.release()
        return -1

    def getLastUpdateTime(self, addr):
        client = self.getClient(addr)
        if client == -1:
            return -1
        return client[2]

    def getLastSequenceNumber(self, addr):
        client = self.getClient(addr)
        if client == -1:
            return -1
        return client[1]

    def remove(self, addr):
        client = self.getClient(addr)
        if client == -1:
            return -1
        self.lock.acquire()
        self.clients.remove(client)
        self.lock.release()
        return addr

    def pushClient(self, addr, seq_num):
        self.lock.acquire()
        self.clients.append((addr, seq_num, time.time()))
        self.lock.release()

    def receivedExistingClientCommunication(self, addr, seq_num):
        client = self.getClient(addr)
        if client == -1:
            return -1

        self.remove(addr)
        self.pushClient(client[0], seq_num)

    # removes any timed out clients from the active client list, returns a list of clients that were removed
    def updateTimeout(self):
        if self.isEmpty():
            return -1
        self.lock.acquire()
        current_time = time.time()
        timeout_clients = []
        for client in self.clients:
            last_packet_time = client[2]
            if (current_time - last_packet_time) >= self.timeout:
                timeout_clients.append(client)
        self.lock.release()

        # potentially issues with locking going on here? maybe bad code for multiple concurrent clients, not sure
        for client in timeout_clients:
            self.remove(client[0])

        return timeout_clients

    def isNewClient(self, addr):
        self.lock.acquire()
        if len(self.clients) == 0:
            self.lock.release()
            return True

        for client in self.clients:
            if client[0] == addr:
                self.lock.release()
                return False
        self.lock.release()
        return True

    def isEmpty(self):
        self.lock.acquire()
        if len(self.clients) == 0:
            self.lock.release()
            return True
        self.lock.release()
        return False

def openConnection(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    return server_socket

def isPacketLoss(seq_num, addr, clients):
    if clients.isNewClient(addr):
        if seq_num != 1:
            return True
        return False

    if seq_num != clients.getLastSequenceNumber(addr)+1:
        return True
    return False

def handleMessage(msg, addr, conn, clients):
    rand = random.randint(0, 10)
    reply = msg.upper().encode("utf-8")
    if rand < 4:
        sys.stdout.write("NOTE simulated packet lost\n")
        return

    # msg_arr[0] = Ping; [1] = sequence number; [2] = time sent
    msg_arr = msg.split(" ")
    seq_num = int(msg_arr[1])
    sys.stdout.write("NOTE sequence number = " + str(seq_num) + '\n')  # note to help see whats happening from console
    time_sent = float(msg_arr[2])
    delay = time.time() - time_sent

    sys.stdout.write("One-way delay for address " + str(addr[0]) + ":" + str(addr[1]) + " = " + str(delay) + '\n')
    if isPacketLoss(seq_num, addr, clients):
        sys.stdout.write("Packet loss detected!\n")

    if clients.isNewClient(addr):
        sys.stdout.write("NOTE new client " + str(addr[0]) + ":" + str(addr[1]) + '\n')  # note to help see from console
        clients.pushClient(addr, seq_num)
        conn.sendto(reply, addr)
        return

    if clients.receivedExistingClientCommunication(addr, seq_num) == -1:
        sys.stdout.write("Error")

    conn.sendto(reply, addr)

def heartbeatUpdate(clients):
    while True:
        if clients.isEmpty():
            continue

        timeout_clients = clients.updateTimeout()
        if timeout_clients == -1:
            continue
        for client in timeout_clients:
            sys.stdout.write(str(client[0][0]) + ':' + str(client[0][1]) + " timed out.\n")


buffer_size = 1024
port_num = 12000
sock = openConnection(port_num)
active_clients = ActiveClientList()

# start heartbeat monitoring thread:
heartbeatThread = threading.Thread(
    target=heartbeatUpdate,
    args=(
        active_clients,
    )
)
heartbeatThread.start()

while True:
    packet = sock.recvfrom(buffer_size)
    message = packet[0].decode("utf-8")
    address = packet[1]
    handleMessage(message, address, sock, active_clients)
