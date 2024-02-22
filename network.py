import socket
import pickle
from client_settings import *
import server_settings


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_settings.SERVER_IP
        self.port = server_settings.SERVER_PORT
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

    def connect(self):
        try:
            self.client.connect(self.server_addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(data.encode())
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


if __name__ == '__main__':
    n = Network()
