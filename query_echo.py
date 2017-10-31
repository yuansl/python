#!/usr/bin/python3

import socket
import asyncio
import datetime

if __name__ == '__main__':
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.connect(('localhost', 8888))
    data = sockfd.recv(1024)
    print(data.decode())
    sockfd.close()
