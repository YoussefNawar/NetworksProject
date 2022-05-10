# echo-server.py

from base64 import decode
import socket
from _thread import *
import threading
print_lock = threading.Lock()
# HOST = input("Enter the server IP : ")
# PORT = input("Enter the server port number :")

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
dir = "./ServerFiles/"

def getTimeOutValue():
    return 5

def parse_request(command):
    x = command.split(' /',1)
    method = x[0]
    x = x[1].split(" ",1)
    file_name = x[0]
    x = x[1].split('\r\n',1)
    protocol = x[0]
    x = x[1].split(':')
    host = x[1]
    port = x[2].split('\r\n\r\n',1)[0]
    if method =="POST":
        file = x[2].split('\r\n\r\n',1)[1].split('\r\n')[0]
        return method, file_name,protocol,host,port,file
    return method, file_name,protocol,host,port,None


def threading(conn):
    data = conn.recv(1024)
    request = data.decode()
    method, file_name,protocol,host,port,file = parse_request(request)
    if protocol == 'HTTP/1.0':
        response = handle_request(conn, method, file_name, file)
        conn.sendall(response.encode())
        print("Closing connection.....")
        conn.close()
        print_lock.release()
    elif protocol =="HTTP/1.1":
        conn.settimeout(getTimeOutValue())
        try:
            while True:
                print("Entered while loop")
                response = handle_request(conn,method,file_name,file)
                conn.sendall(response.encode())
                data = conn.recv(1024)
                request = data.decode()
                # method, file_name,protocol,host,port,file = parse_request(request)
        except socket.timeout as e:
            print("Time out!")
            print("Closing connection.....")
            conn.close()
            print_lock.release()
            return

def handle_request(conn, method, file_name,file):
    if method == "GET":
        try:
            f = open(f"{dir}{file_name}", mode="r")
            print("Reading file")
            file_read = f.read()
            f.close()  # Send HTTP response
            response = 'HTTP/1.0 200 OK\r\n' + file_read +'\r\n\r\n'
            return response
        except IOError:
            print("IO Error")
            response = 'HTTP/1.0 404 NOT FOUND\r\n'
            return response
    elif method =='POST':
        data = file
        f = open(f"{dir}/{file_name}", "a")
        f.write(data)
        f.close()
        response = 'HTTP/1.0 200 OK\r\n'
        return response

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HOST = "127.0.0.1"
    PORT = 65432
    print("Starting Server....")
    s.bind(("127.0.0.1", 65432))
    s.listen()
    print(f"Socket is bind to {HOST}:{PORT}")
    #conn, addr = s.accept()
    while True:
        conn, addr = s.accept()
        # conn.settimeout()
        print(f"Connected by {addr}")
        print_lock.acquire()
        start_new_thread(threading,(conn,))


