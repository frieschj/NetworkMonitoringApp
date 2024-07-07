# Author: John Friesch
# GitHub username: frieschj
# Date: 
# Description:

import socket


def tcp_client(input_message):
    # Create a Socket:
    # socket(): Create a TCP/IP socket using AF_INET for IPv4 and SOCK_STREAM for TCP
    sock = socket.socket(socket.AF_INET)

    # Specify Server Address and Port:
    # Define the server's IP address and port number to connect to
    server_address = '127.0.0.1'
    server_port = 12345

    try:
        # Establish a Connection:
        # connect(): Connect the socket to the server's address and port
        sock.connect((server_address, server_port))

        # Send and Receive Data:
        # sendall(): Send data to the server
        message = input_message
        print(f"Sending: {message}")
        sock.sendall(message.encode())

        # If message IS "Goodbye", server doesn't send anything back
        if message != "Goodbye":
            response = sock.recv(1024)
            print(f"Received: {response.decode()}")

    finally:
        # Close the Connection:
        # close(): Close the socket to free up resources
        sock.close()
