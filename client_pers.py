# echo-client.py

import socket
from time import sleep

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 65432  # The port used by the server
dir = "./ClientFiles"

def parse_file(file_name):
    f = open(f"{file_name}", mode = "r")
    commands = f.read().split("\n")
    f.close()
    return commands

def parse(cmd):
    x = cmd.split()
    method = x[0]
    file_name = x[1]
    host = x[2]
    if len(x) > 3:
        port = x[3]
        return method,file_name,host,port
    return method,file_name,host,80

commands = parse_file("commands.txt")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((str("127.0.0.1"), int(65433)))
    print(f"Starting socket connection with 127.0.0.1:65433")
    for i in commands:
        method , file_name, HOST, PORT = parse(i)
        if method == "GET":
            request = f"{method} /{file_name} HTTP/1.1\r\nHOST: {HOST}:{PORT}\r\n\r\n" 
            print(request)
            s.sendall(request.encode())
            #print("Waiting for data from server....")
            data = b''
            #s.setblocking(False)
            
        elif method == "POST":
            try:       
                f = open(f"{dir}/{file_name}",mode ="r")
                file = f.read()
                f.close()
                request = f"POST /{file_name} HTTP/1.1\r\nHOST:{HOST}: {PORT}\r\n\r\n{file}\r\n" 
                s.sendall(request.encode())
            except IOError:
                print("FILE NOT FOUND")
        # sleep(5)
        sleep(2)
    while True:
        print("Waiting for data from server....")
        buf = s.recv(1024) 
        if not buf:
            break
        data += buf
    print(f"{data}")
# sleep(10)
s.close()

