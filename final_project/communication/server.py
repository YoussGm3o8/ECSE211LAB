import socket
"""
This tool is used for the raspberry pi to send data to a computer.
(This script is the server side of the communication e.g. your computer)
It allows computers to better process the data if needed for debugging and interpretation purposes.

NOTE: this should not be used in the final product. This is only for debugging purposes
"""
HOST = '0.0.0.0'
PORT = 22005

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))

        self.server_socket.listen(5)
        print('Server is listening on {}:{}'.format(HOST, PORT))

        self.client_socket, self.client_address = self.server_socket.accept()
        print('Connected to {}'.format(self.client_address))


    def __iter__(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                yield data.decode()

                response = '0'
                self.client_socket.send(response.encode())
        except KeyboardInterrupt as KI:
            print("KeyboardInterrupt")
        finally:
            self.client_socket.close()
            self.server_socket.close()
            print('Connection closed')
