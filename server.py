# echo-server.py

import socket
from _thread import *
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def parse_command(command):
    x = command.split()
    method = x[0]
    file_name = x[1]
    return method , file_name
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            request = decode
            if not data:
                break
            conn.sendall(data)