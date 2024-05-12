import socket
import struct
import marshal
import threading

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8080

class MulticastListenerThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            received_data = self.sock.recv(10240)
            received_dict = marshal.loads(received_data)
            received_dict['sender_ip'] = socket.inet_ntoa(received_data[0:4])  # Extract sender's IP address
            print(f"received: {received_dict}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

listener_thread = MulticastListenerThread(sock)
listener_thread.start()