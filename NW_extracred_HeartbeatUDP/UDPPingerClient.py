import math
import socket
import time

def openConnection(time_out):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(time_out)
    return client_socket

def sendMessage(conn, seq_num):
    msg = "Ping " + str(seq_num) + ' ' + str(time.time())
    byte_msg = msg.encode("utf-8")
    conn.sendto(byte_msg, server_address)

def awaitReply(conn, size):
    try:
        msg_from_server = conn.recvfrom(size)[0].decode("utf-8")
        print("Response: ", msg_from_server)
        return time.time()
    except socket.timeout:
        print("Request timed out")
        return -1


timeout = 1
sock = openConnection(timeout)
server_address = ("127.0.0.1", 12000)
buffer_size = 1024

min_rtt = math.inf
max_rtt, sum_rtt, num_success, percent_loss = 0, 0, 0, 0.0
for i in range(1, 11):
    send_time = time.time()
    sendMessage(sock, i)

    reply_time = awaitReply(sock, buffer_size)
    if reply_time != -1:
        rtt = reply_time - send_time
        print("rtt: ", rtt)

        num_success += 1
        sum_rtt += rtt
        if rtt < min_rtt:
            min_rtt = rtt
        if rtt > max_rtt:
            max_rtt = rtt
        avg_rtt = sum_rtt / num_success

        print("min rtt: ", min_rtt)
        print("max rtt: ", max_rtt)
        print("avg rtt: ", avg_rtt)

    if num_success != 0:
        percent_loss = (1-(num_success/i)) * 100

    print("% packet loss: ", percent_loss, "%\n")