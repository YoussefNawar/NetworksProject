# echo-client.py

import socket
from time import sleep
from traceback import print_tb

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
    ext = x[1].split(".")[1]
    method = x[0]
    file_name = x[1]
    host = x[2]
    if len(x) > 3:
        port = x[3]
        return method,file_name,host,port,ext
    return method,file_name,host,80,ext

commands = parse_file("commands.txt")
for i in commands:
    method , file_name, HOST, PORT, EXT = parse(i)
    request = f"{method} /{file_name} HTTP/1.0\r\nHOST: {HOST}:{PORT}\r\n\r\n"
    if request in cache:
        if EXT == "png":
            print("This file is located in the  cache")
            x = cache.get(request)
            #print(x)

            x1 = x.split(b"\r\n\r\n")[0].decode()
            print(x1)
            x2 = x.split(b"\r\n\r\n")[1]
            print(x2)
            #f = open(f"{dir}/{file_name}", mode="rb")
            #file = f.read()
            #f.close()
        else:

            print("This file is located in the  cache")
            x = cache.get(request)
            x1 = x.split("\r\n\r\n")[0]
            print(x1)
            x2 = x.split("\r\n\r\n")[1]
            print(x2)
           # f = open(f"{dir}/{file_name}", mode="r")
           # file = f.read()
           # f.close()

                
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Starting socket connection with {HOST}:{PORT}")
            s.connect((str(HOST), int(PORT)))
            if method == "GET":
               # request = f"{method} /{file_name} HTTP/1.1\r\nHOST: {HOST}:{PORT}\r\n\r\n"
                s.sendall(request.encode())
                data = s.recv(100000)
                print("Waiting for data from server....")
                
                if EXT == "png":
                    f = open(f"{dir}/{file_name}", mode="wb+")
                    file_png = data.split(b"\r\n\r\n")[1]
                    file = f.write(file_png)
                    f.close()
                    cache[request]=data
                else:
                    f = open(f"{dir}/{file_name}", mode="w")
                    content = data.split(b"\r\n\r\n")[1]
                    file = f.write(content.decode())
                    f.close()
                    cache[request]=data.decode()

                #print(f"{data.decode()}")
                
            elif method == "POST":
                try:       
                    if EXT == "png":
                        f = open(f"{dir}/{file_name}", mode="rb")
                        file = f.read()
                        f.close()
                        request = f"POST /{file_name} HTTP/1.0\r\nHOST: {HOST}:{PORT}\r\n\r\n"
                        request = request.encode()
                        request = request + file + b"\r\n"
                    else:
                        f = open(f"{dir}/{file_name}",mode ="r")
                        file = f.read()
                        f.close()
                        request = f"POST /{file_name} HTTP/1.0\r\nHOST: {HOST}:{PORT}\r\n\r\n{file}\r\n" 
                        request = request.encode()
                    s.sendall(request)
                except IOError:
                    print("FILE NOT FOUND")
            # sleep(10)

