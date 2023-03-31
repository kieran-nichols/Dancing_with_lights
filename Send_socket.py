import socket
import time
import pickle
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

##while(True):
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    while(True):
#        s.connect((HOST, PORT))
#        #s.sendall(b"Hello, world")
#        #s.sendall(array)
#        arr1 = [1,2,3,4]
#        arr2 = [0,1]
#        data = json.dumps({"arr1": arr1, "arr2": arr2})
#        s.send(data.encode())
#        #data = s.recv(1024)
#        #data_arr = json.loads(data.decode())
        
#        print(f"Received {data!r}")
#        time.sleep(1)
#        s.close()
        
# echo-server.py

# ...

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)