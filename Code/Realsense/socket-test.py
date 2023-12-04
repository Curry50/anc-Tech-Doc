#!/usr/bin/env python
# -*- coding: utf-8 -*

import socket, struct, os
from time import sleep
import numpy as np
import matplotlib.pyplot as plt


def UDP_Send():
    # -------------------------------- Initializing --------------------------------------------
    # Create a socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serveraddr = ("127.0.0.1", 9202)
    udp_socket.connect(serveraddr)
    count = 0
    # Create an increment for while loop
    while count < 100:
        send_msg_code = struct.pack("6d", 1.1,1.2,1.3,1.4,1.5,1.6) #对应Simulin的六路数据接收
        udp_socket.sendto(send_msg_code, serveraddr)
        count += 1
        print(send_msg_code)
        sleep(1)
    # Close the udp socket.
    udp_socket.close()


if __name__ == "__main__":
    UDP_Send()

