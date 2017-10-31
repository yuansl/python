#!/usr/bin/python3

import socket
import asyncio
import datetime
import threading

def create_server():
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    sockfd.bind(('localhost', 8888))
    sockfd.listen(128)    
    return sockfd

def accept_connection(sockfd, loop):
    connfd, peer_addr = sockfd.accept()
    connfd.send(str(datetime.datetime.now()).encode())
    connfd.close()

def echo_server_fashion1():
    sockfd = create_server()        
    while True:
        connfd, peer_addr = sockfd.accept()
        connfd.send(str(datetime.datetime.now()).encode('utf-8'))
        connfd.close()

def echo_server_fashion2():
    sockfd = create_server()
    loop = asyncio.get_event_loop()
    loop.add_reader(sockfd, accept_connection, sockfd, loop)
    loop.run_forever()
    loop.close()

class EchoServer(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        sockfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,True)
        sockfd.bind(('localhost', 8888))
        sockfd.listen(128)
        while True:
            connfd, peer_addr = sockfd.accept()
            connfd.send(str(datetime.datetime.now()).encode('utf-8'))
            connfd.close()

def echo_server_fashion3():
    threads = []
    for i in range(0, 128):
        t = EchoServer()
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    echo_server_fashion3()
