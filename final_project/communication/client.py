import socket

"""
This tool is used for the raspberry pi to send data to a computer.
(This script is the client side of the communication e.g. the raspberry pi)
It allows computers to better process the data if needed for debugging and interpretation purposes.

NOTE: this should not be used in the final product. This is only for debugging purposes
"""


SERVER_IP = '192.168.50.154'
PORT = 22005


class Client:
    def __init__(self):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, PORT))
        print('Connected to server {} using port {}'.format(SERVER_IP, PORT))
    
    def send(self, message : str) -> str:
        if len(message) > 1024:
            return 'Message was not sent because it is too long. Maximum length is 1024 bytes.'

        self.client_socket.send(message.encode())
        response = self.client_socket.recv(1024).decode()
        return response

    def exit(self):
        self.client_socket.close()
        print('Connection closed')
