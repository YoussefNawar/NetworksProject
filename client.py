# echo-client.py

import socket

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 65432  # The port used by the server
# dir = "/Users/youssefnawar/PycharmProjects/NetworksProject/"

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
for i in commands:
    method , file_name, HOST, PORT = parse(i)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(HOST)
        print(PORT)
        s.connect((str(HOST), int(PORT)))
        request = f"{method} {file_name} HTTP/1.0" 
        s.sendall(bytes(request,"utf-8"))
        if method is "GET":
            data = s.recv(1024)
            print(f"Received {data!r}")
        elif method is "POST":
            try:
                f = open(f"{file_name}",mode ="r")
                file = f.read()
                f.close()
                s.sendall(bytes(file,"utf-8"))
            except IOError:
                print("FILE NOT FOUND")
        s.close()
