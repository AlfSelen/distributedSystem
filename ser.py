import socket

server_ip, port = "127.0.0.1", 5555
print(socket.gethostname())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip, port))
s.listen(5)
while True:

    try:
        cli_connection, cli_address = s.accept()
        print(f"Connection: {cli_connection}")
        cli_connection.send(bytes("Welcome to server", "utf-8"))

        raw_data = cli_connection.recv(1024)
        print(f"{type(raw_data)=}, {len(raw_data)=}")
        rec_byte = raw_data[0]
        print(f"{rec_byte.=}")
        msg = raw_data[1:].decode("utf-8")
        print(f"{msg=}")

        raw_data = cli_connection.recv(1024)
        rec_byte = raw_data[0]
        print(f"{rec_byte=}")
        msg = raw_data[1:].decode("utf-8")
        print(f"{msg=}")

        raw_data = cli_connection.recv(1024)
        rec_byte = raw_data[0]
        print(f"{rec_byte=}")
        msg = raw_data[1:].decode("utf-8")
        print(f"{msg=}")

        raw_data = cli_connection.recv(1024)
        rec_byte = raw_data[0]
        print(f"{rec_byte=}")
        msg = raw_data[1:].decode("utf-8")
        print(f"{msg=}")

    except Exception as e:
        print(e)
        s.close()
        break
