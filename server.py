# echo-server.py

from base64 import decode
import socket
from _thread import *
import threading
print_lock = threading.Lock()
HOST = input("Enter the server IP : ")
PORT = input("Enter the server port number :")

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
#dir = "/ServerFiles"

def getTimeOutValue():
    return 10

def parse_request(command):
    x = command.split(' /',1)
    method = x[0]
    x = x[1].split(" ")
    file_name = x[0]
    x = x[1].split('\r\n',1)
    protocol = x[0]
    x = x[1].split(':')
    host = x[1]
    port = x[2].split('\r\n\r\n')[0]
    if method =="POST":
        file = x[2].split('\r\n\r\n')[1].split('\r\n')[0]
        return method, file_name,protocol,host,port,file
    return method, file_name,protocol,host,port,None

# lis= parse_request("POST /kosom_sengab HTTP/1.0\r\nHOST:127.0.0.1:80\r\n\r\nekjntngiuvieklnbie\r\n")
# print(lis)

def threading(conn):
    data = conn.recv(1024)
    if not data:
        print_lock.release()
        return
    request = data.decode()
    method, file_name,protocol,host,port,file = parse_request(request)
    if protocol == 'HTTP/1.0':
        handle_request(conn, method, file_name, file)
        conn.close()
        print("Closing connection.....")
    elif protocol =="HTTP/1.1":
        conn.settimeout(getTimeOutValue)
        try:
            while True:
                response = handle_request(conn,method,file_name,file)
                conn.sendall(response.encode())
                request = conn.recv(4096)
                method, file_name,protocol,host,port,file = parse_request(request)
        except socket.timeout as e:
            print("Time out!")
            print("Closing connection.....")
            conn.close()
        pass

def handle_request(conn, method, file_name,file):
    if method == "GET":
        try:
            f = open(f"{file_name}", mode="r")
            file_read = f.read()
            f.close()  # Send HTTP response
            response = 'HTTP/1.0 200 OK\r\n' + file_read +'\r\n\r\n'
            return response
        except IOError:
            response = 'HTTP/1.0 404 NOT FOUND\r\n'
            return response
    elif method =='POST':
        data = file
        f = open(f"{file_name}", "a")
        f.write(data.decode())
        f.close()
        response = 'HTTP/1.0 200 OK\r\n'
        return response

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting Server....")
    s.bind((HOST, PORT))
    s.listen()
    print(f"Socket is bind to {HOST}{PORT}")
    #conn, addr = s.accept()
    while True:
        conn, addr = s.accept()
        # conn.settimeout()
        print_lock.acquire()
        print(f"Connected by {addr}")
        start_new_thread(threading,(conn,))

