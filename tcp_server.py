# Author: John Friesch
# GitHub username: frieschj
# Date: 
# Description:

import socket
import network_monitoring_app
def tcp_server():
    # Create a Socket:
    # socket(): Create a TCP/IP socket using AF_INET for IPv4 and SOCK_STREAM for TCP
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the Socket:
    # bind(): Bind the socket to a specific IP address and port
    server_address = '127.0.0.1'    # Localhost
    server_port = 12345             # Port to listen on
    server_sock.bind((server_address, server_port))
    # Listen for Incoming Connections:
    # listen(): Put the socket into server mode and listen for incoming connections
    server_sock.listen(5)   # Argument is the backlog of connections allowed
    print("Server is listening for incoming connections...")
    while True:
        # Accept Connections:
        # accept(): Accept a new connection
        client_sock, client_address = server_sock.accept()
        print(f"Connection from {client_address}")
        try:
            # Send and Receive Data:
            # recv(): Receive data from the client
            message = client_sock.recv(1024)
            print(f"Received message: {message.decode()}")
            # If client sends "Goodbye", close the client connection and server socket
            if message.decode() == "Goodbye":
                client_sock.close()
                print(f"Connection with {client_address} closed")
                server_sock.close()
                print("Server socket closed")
                break
            # sendall(): Send a response back to the client
            response = f"Message received"
            client_sock.sendall(response.encode())
        finally:
            # Close Client Connection:
            # close() (on the client socket): Close the client connection
            client_sock.close()
            print(f"Connection with {client_address} closed")

