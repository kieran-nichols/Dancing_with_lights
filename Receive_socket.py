# echo-server.py

import socket
import time
import json

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

#while(True):
#    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#        s.bind((HOST, PORT))
#        s.listen()
#        conn, addr = s.accept()
#        with conn:
#            print(f"Connected by {addr}")
#            while True:
#                data = conn.recv(1024)
#                data = json.loads(data.decode())
#                arr1 = data.get("arr1")
#                arr2 = data.get("arr2")
#                print("arr1: ", arr1, ", arr2: ", arr2)
#                if not data:
#                    break
#                #conn.sendall(data)
#    time.sleep(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")