# echo-server.py

import socket
from _thread import *
import threading
print_lock = threading.Lock()
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def parse_command(command):
    x = command.split()
    method = x[0]
    file_name = x[1]
    return method, file_name
def threading(conn):
    while True:
        data = conn.recv(1024)
        request = data.decode
        method, file_name = parse_command(request)
        if method is "GET":
            f = open(f"{file_name}", mode="r")
            file = f.read()
            f.close()  # Send HTTP response
            response = 'HTTP/1.0 200 OK\n\n' + file
            conn.sendall(response.encode())
        if not data:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    #conn, addr = s.accept()
    while True:
        conn, addr = s.accept()
        print_lock.acquire()
        with conn:
            print(f"Connected by {addr}")
            threading(conn)
    s.close
        # while True:
        #     data = conn.recv(1024)
        #     request = data.decode
        #     method, file_name = parse_command(request)
        #     if method is "GET":
        #         f = open(f"{file_name}",mode ="r")
        #         file = f.read()
        #         f.close()# Send HTTP response
        #         response = 'HTTP/1.0 200 OK\n\n' + file
        #         conn.sendall(response.encode())

            # if not data:
            #     break
