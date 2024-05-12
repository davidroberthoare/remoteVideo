import socket
from time import sleep, time
import marshal

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8080
MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

def broadcast(data_dict):
    data_dict['timestamp'] = time()
    try:
        sock.sendto(marshal.dumps(data_dict), (MCAST_GRP, MCAST_PORT))
    except Exception as e:
        print(f"Error sending data: {e}")

while True:
    print("sending multicast packet...")
    message = {"hello": "world"}
    broadcast(message) 
    sleep(2)