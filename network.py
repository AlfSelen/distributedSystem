import socket
import pickle
from client_settings import *
import server_settings


class Network:
    def __init__(self, server_ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip if server_ip else "127.0.0.1"
        self.port = port if port else 5555
        self.server_addr = (self.server, self.port)
        self.new_connection_data = self.connect()

    def getPlayers(self, player):
        try:
            self.client.send(pickle.dumps(player))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def getConnectionData(self):
        return self.new_connection_data

    def initialConnect(self):
        self.client.connect(self.server_addr)
        return pickle.loads(self.client.recv(2048))

    def connect(self):
        try:
            connect_response = self.client.connect(self.server_addr)
            # print(f"{connect_response}:{type(connect_response)}")
            server_response = self.client.recv(2048)
            # print(f"{server_response}:{type(server_response)}")
            return pickle.loads(server_response)
        except ConnectionResetError as e:
            if e.winerror == 10054:
                print(f"Server disconnected")
            if e.winerror == 10061:
                print("Could not connect to server, make sure IP and port is correct and that server is running (WinError 10061)")
            else:
                print(f"Unexpected connection reset error {e}")
        except Exception as e:
            print(f"Unknown network error {e}")

    def send(self, data):
        try:
            self.client.sendall(data.encode())
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def sendTextReceivePickle(self, data):
        try:
            self.client.sendall(data.encode())
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)


if __name__ == '__main__':
    n = Network()
