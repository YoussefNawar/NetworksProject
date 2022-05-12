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
    if file_name in cache:
                print("This file is located in the  cache")
                f = open(f"{dir}/{file_name}", mode="r")
                file = f.read()
                print(file)
                f.close()
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Starting socket connection with {HOST}:{PORT}")
            s.connect((str(HOST), int(PORT)))

            if method == "GET":
                request = f"{method} /{file_name} HTTP/1.0\r\nHOST: {HOST}:{PORT}\r\n\r\n"
                s.sendall(request.encode())
                data = s.recv(100000)
                print("Waiting for data from server....")
                
                if EXT == "png":
                    f = open(f"{dir}/{file_name}", mode="a")
                    header = data.split(b"\r\n\r\n")[0]
                    file = f.write(header.decode())
                    f.close()
                    f = open(f"{dir}/{file_name}", mode="wb+")
                    file_png = data.split(b"\r\n\r\n")[1]
                    file = f.write(file_png)
                    f.close()
                else:
                    f = open(f"{dir}/{file_name}", mode="a")
                    file = f.write(data.decode())
                    f.close()

                
                #print(f"{data.decode()}")
                cache[file_name]=dir
            elif method == "POST":
                try:       
                    if EXT == "png":
                        f = open(f"{dir}/{file_name}", mode="rb")
                        file = f.read()
                        f.close()
                        request = f"POST /{file_name} HTTP/1.0\r\nHOST: {HOST}:{PORT}\r\n\r\n"
                        request = request.encode()
                        request = request + file 
                    else:
                        f = open(f"{dir}/{file_name}",mode ="r")
                        file = f.read()
                        f.close()
                        request = f"POST /{file_name} HTTP/1.0\r\nHOST: {HOST}:{PORT}\r\n\r\n{file}" 
                        request = request.encode()
                    s.sendall(request)
                except IOError:
                    print("FILE NOT FOUND")
            # s.close()
            sleep(10)

