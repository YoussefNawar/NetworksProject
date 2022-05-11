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
cache = {}

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
for i in commands:
    method , file_name, HOST, PORT = parse(i)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Starting socket connection with {HOST}:{PORT}")
        s.connect((str(HOST), int(PORT)))
        if method == "GET":
            if file_name in cache:
                print("This file is located in the  cache")
                f = open(f"{dir}/{file_name}", mode="r")
                file = f.read()
                print(file)
                f.close()

            else:

                request = f"{method} /{file_name} HTTP/1.0\r\nHOST:{HOST}:{PORT}\r\n\r\n"

                s.sendall(request.encode())
                data = s.recv(4096)
                print("Waiting for data from server....")
                print(f"{data.decode()}")
                cache.update(file_name)
        elif method == "POST":
            try:       
                f = open(f"{dir}/{file_name}",mode ="r")
                file = f.read()
                f.close()
                request = f"POST /{file_name} HTTP/1.0\r\nHOST:{HOST}:{PORT}\r\n\r\n{file}" 
                s.sendall(request.encode())
            except IOError:
                print("FILE NOT FOUND")
        # s.close()
        sleep(10)

