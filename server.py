# echo-server.py

from base64 import decode
import socket
from _thread import *
import threading
from time import sleep
from numpy import not_equal
print_lock = threading.Lock()
# HOST = input("Enter the server IP : ")
# PORT = input("Enter the server port number :")

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
dir = "./ServerFiles"
counter = 0
def getTimeOutValue():
    return int(10 / counter)

def parse_multiple_requests(requests):
    my_list = []
    while len(requests) != 0:
        try:
            h = requests.index(b"GET")
        except ValueError:
            h = -1
        if h >= 0:
            request = requests.split(b"\r\n\r\n",1)
            x = request[0]+b"\r\n\r\n"
            my_list.append(x)
            requests = request[1]
        else:
            try:
                h = requests.index(b"png")
            except ValueError:
                h = -1
            if h == -1:
                request = requests.split(b"\r\n",4)
                x = request[0]+b"\r\n"+request[1]+b"\r\n\r\n"+request[3]+b"\r\n"
                my_list.append(x)
                try:
                    requests = request[4]
                except IndexError:
                    break    
            else:
                # print(requests)
                request = requests.split(b"\r\n",5)
                x = request[0]+b"\r\n"+request[1]+b"\r\n\r\n"+request[3]+request[4]+b"\r\n"
                my_list.append(x)
                try:
                    requests = request[5]
                except IndexError:
                    break         
    return my_list

def parse_request(command):
    x = command.split(' /',1)
    method = x[0]
    y = x[1].split(" ",2)
    file_name = y[0]
    protocol = y[1].split('\r\n')[0]
    x = y[2].split('\r\n\r\n')
    # host = x[1]
    # port = x[2].split('\r\n\r\n',1)[0]
    #if method =="POST":
     #   file = x[1]
     #   return method, file_name,protocol,None,None,file
    return method, file_name,protocol,None,None

def pipeline(data,conn):
    my_list = parse_multiple_requests(data)
    for i in my_list:
        data = i
        request = data.split(b"\r\n\r\n")
        method, file_name,protocol,host,port = parse_request(request)
        file = data.split(b"\r\n\r\n")[1]
        response = handle_request(conn,method,file_name,file)
        conn.sendall(response)
        print("Response is sent")

    # request = data.split(b"\r\n\r\n")[0].decode()
    #data = data.decode()
    # if request:
    #     #print(data)
    #     method, file_name,protocol,host,port = parse_request(request)
    #     file = data.split(b"\r\n\r\n")[1]
    #     response = handle_request(conn,method,file_name,file)
    #     conn.sendall(response)
    #     #i = i + 1
    return
        
def threading(conn,counter):
    data = conn.recv(100000)
    my_list = parse_multiple_requests(data)
    data = my_list[0]
    # print(data)
    request = data.split(b"\r\n\r\n")[0].decode()
    # print(request)
    method, file_name,protocol,host,port = parse_request(request)
    file = data.split(b"\r\n\r\n")[1]
    my_list = my_list[1:]
    #print(parse_request(request))
    if protocol == 'HTTP/1.0':
        response = handle_request(conn, method, file_name, file)
        conn.sendall(response)
        print("Closing connection.....")
        conn.close()
        print_lock.release()
    elif protocol =="HTTP/1.1":
        response = handle_request(conn,method,file_name,file)
        conn.sendall(response)
        print("Response is sent")
        for i in my_list:
            data = i
            request = data.split(b"\r\n\r\n")[0].decode()
            method, file_name,protocol,host,port = parse_request(request)
            file = data.split(b"\r\n\r\n")[1]
            response = handle_request(conn,method,file_name,file)
            conn.sendall(response)
            print("Response is sent")
        conn.settimeout(getTimeOutValue())
        data =b''
        # print(counter)
        try: 
            while True:       
                conn.settimeout(getTimeOutValue())
                print("Entered while loop")
                data = conn.recv(1024)
                start_new_thread(pipeline,(data,conn))
        except socket.timeout as e:
            # for k in response1:
            #     print(k)
            #     conn.sendall(k)
            counter = counter - 1
            print("Time out!")
            print("Closing connection.....")
            conn.close()
            print_lock.release()
            return


def handle_request(conn, method, file_name,file):
    if method == "GET":
        try:
            ext = file_name.split(".")[1]
            print("Reading file")
            if ext == "png":
                f = open(f"{dir}/{file_name}", mode="rb")
                file_read = f.read()
                f.close()  # Send HTTP response
                response = 'HTTP/1.1 200 OK\r\n\r\n'
                response = response.encode()    
                response = response  + file_read + b"\r\n"
            else:
                f = open(f"{dir}/{file_name}", mode="r")
                file_read = f.read()
                f.close()  # Send HTTP response
                response = 'HTTP/1.1 200 OK\r\n\r\n' + file_read +"\r\n"
                response =response.encode()
            print(f"file {file_name} is sent")
            return response
        except IOError:
            print("IO Error")
            response = 'HTTP/1.1 404 NOT FOUND\r\n\r\n'
            print(response)
            return response
    elif method =='POST':
        ext = file_name.split(".")[1]
        if ext == "png":
            f = open(f"{dir}/{file_name}", mode="wb+")
            file = f.write(file)
            f.close()
        else:
            data = file
            f = open(f"{dir}/{file_name}", "w")
            print("nvdolrfi")
            f.write(data.decode())
            f.close()
        response = 'HTTP/1.1 200 OK\r\n\r\n'
        print(response)
        return response.encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HOST = "127.0.0.1"
    PORT = 65432
    print("Starting Server....")
    s.bind(("127.0.0.1", 65433))
    #s.listen()
    print(f"Socket is bind to {HOST}:{PORT}")
    #conn, addr = s.accept()
    while True:
        s.listen()
        conn, addr = s.accept()
        counter = counter + 1
        # conn.settimeout()
        print(f"Connected by {addr}")
        print_lock.acquire()
        start_new_thread(threading,(conn,counter))

# habal = parse_request("POST /tesrwvrt.txt HTTP/1.1\nContent-Type: text/plain\nPostman-Token: 8952b183-6f71-4ea7-93d9-ebcfe207b717\nHost: 127.0.0.1:65432\nContent-Length: 13\r\n\r\nkjbrvsnvkrsnv")
# print(habal)
# requests = b"GET /alo.png HTTP/1.1\r\nHOST: 127.0.0.1:65433\r\n\r\nGET /sora.png HTTP/1.1\r\nHOST: 127.0.0.1:65433\r\n\r\nPOST /test.txt HTTP/1.1\r\nHOST:127.0.0.1: 65433\r\n\r\nsengab 5awl fash5 \n\nHTTP/1.1 200 OK\r\nGET /test.txt HTTP/1.1\r\nHOST: 127.0.0.1:65433\r\n\r\n"
# my_list = parse_multiple_requests(requests)
# print(my_list)


