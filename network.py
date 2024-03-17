import socket
import pickle
from client_settings import *
import server_settings
from board import Board
from player import Player


# from check import


def load_data(data):
    try:
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError:
            try:
                return data.decode()
            except UnicodeDecodeError as e:
                print(f"Format of data is wrong {e}")
                return data
    except socket.error as e:
        print(e)


def send_data(conn: socket.socket, data):
    try:
        if isinstance(data, str):
            return conn.sendall((data.encode()))
        elif isinstance(data, (dict, list, tuple, Board, Player)):
            return conn.sendall(pickle.dumps(data))
        else:
            print(f"{data}:{type(data)}")
            raise TypeError("Unsupported data type for sending")
    except socket.error as e:
        print(e)
    except TypeError as e:
        print(e)


def receive_data(conn: socket.socket):
    try:
        return conn.recv(2048)
    except socket.error as e:
        print(e)


def receive(conn: socket.socket):
    return load_data(receive_data(conn))


class Network:
    def __init__(self, server_ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip if server_ip else "127.0.0.1"
        self.port = port if port else 5555
        self.server_addr = (self.server, self.port)

    def receive(self):
        try:
            return self.socket.recv(2048)
        except socket.error as e:
            print(e)

    def initial_send(self, data):
        if isinstance(data, str):
            self.socket.sendall(data.encode())
        elif isinstance(self, (dict, list, tuple)):
            self.socket.sendall(pickle.dumps(data))

    def send_and_receive(self, data):
        try:
            if isinstance(data, str):
                # server_response = self.receive_data(self.socket.sendall(('s', data.encode())))
                server_response = load_data(self.socket.sendall(data.encode()))
            elif isinstance(data, (dict, list, tuple)):
                server_response = load_data(self.socket.sendall(pickle.dumps(data)))
            else:
                raise TypeError("Unsupported data type for sending")
            return server_response
        except socket.error as e:
            print(e)
        except TypeError as e:
            print(e)

    def initialConnect(self):
        self.socket.connect(self.server_addr)
        return pickle.loads(self.socket.recv(2048))

    # def send(self, data):
    #     try:
    #         self.socket.sendall(data.encode())
    #         return self.socket.recv(2048).decode()
    #     except socket.error as e:
    #         print(e)

    def close(self):
        self.socket.close()


class ServerNetwork(Network):
    def __init__(self, server_ip, port, max_backlog_connections=5):
        super().__init__(server_ip, port)
        self.max_backlog_connections = max_backlog_connections
        try:
            self.socket.bind((server_ip, port))
            self.socket.listen(max_backlog_connections)
            # print(f"Server bound to {server_ip}:{port}")
        except socket.error as e:
            print(f"Could not bind {server_ip}:{port}: {e}")

    def listen(self):
        self.socket.listen(self.max_backlog_connections)

    def accept(self):
        return self.socket.accept()


class ClientNetwork(Network):
    def __init__(self, server_ip, port):
        super().__init__(server_ip, port)
        self.new_connection_data = self.connect()

    def getPlayers(self, player):
        try:
            self.socket.sendall(pickle.dumps(player))
            return pickle.loads(self.socket.recv(2048))
        except socket.error as e:
            print(e)

    def connect(self):
        try:
            self.socket.connect(self.server_addr)
            server_response = pickle.loads(self.receive())
            return server_response
        except ConnectionResetError as e:
            if e.winerror == 10054:
                print(f"Server disconnected")
            if e.winerror == 10061:
                print("Could not connect to server, make sure IP and port is correct and that server is running (WinError 10061)")
            else:
                print(f"Unexpected connection reset error {e}")
            return None
        except Exception as e:
            print(f"Unknown network error {e}")
            return None

    def getConnectionData(self):
        return self.new_connection_data


if __name__ == '__main__':
    n = ServerNetwork("10.0.0.4", 5555)
    connection, cli_address = n.accept()
    print(connection, cli_address)
    n.initial_send(pickle.dumps(["A", "B"]))
    game_selection = n.receive()
