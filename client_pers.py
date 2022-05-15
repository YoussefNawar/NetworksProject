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
    ext = x[1].split(".")[1]
    method = x[0]
    file_name = x[1]
    host = x[2]
    if len(x) > 3:
        port = x[3]
        return method,file_name,host,port,ext
    return method,file_name,host,80,ext

commands = parse_file("commands.txt")
list_ext=[]
list_names=[]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((str("127.0.0.1"), int(65433)))
    print(f"Starting socket connection with 127.0.0.1:65433")
    for i in commands:
        method , file_name, HOST, PORT, EXT = parse(i)
        list_ext.append(EXT)
        list_names.append(file_name)
        if method == "GET":
            request = f"{method} /{file_name} HTTP/1.1\r\nHOST: {HOST}:{PORT}\r\n\r\n" 
            print(request)
            s.sendall(request.encode())
            #print("Waiting for data from server....")
            data = []
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
        # sleep(1)
    while True:
        print("Waiting for data from server....")
        buf = s.recv(100000) 
        # print(buf)
        if not buf:
            print("Connection closed")
            break
        data.append(buf)
    #print(f"{data[0]}")
    k=0
    for j in data :
        EXT = list_ext[k]
        file_name = list_names[k]
        k = k + 1
        if str(EXT) == "png":
            f = open(f"{dir}/{file_name}", mode="wb+")
            file_png = j.split(b"\r\n\r\n")[1]
            file = f.write(file_png)
            f.close()
            cache[request]=j
        else:
            f = open(f"{dir}/{file_name}", mode="w")
            content = j.split(b"\r\n\r\n")[1]
            file = f.write(content.decode())
            f.close()
            cache[request]=j.decode()
# sleep(10)
s.close()

