import socket


def add_control_byte(data: bytes, control_byte_string_repr: bytes = b"0x0") -> bytes:
    bit_str = control_byte_string_repr.decode()
    if bit_str.startswith("0b"):
        base = 2
    elif bit_str.startswith("0x"):
        base = 16
    else:
        raise ValueError(f"Unsupported format. Only binary (0b) and hexadecimal (0x) are supported. {bit_str=}")

    bit_int = int(bit_str, base)
    control_byte = bit_int.to_bytes(1, byteorder="big")
    return control_byte + data


def byte_to_bits(byte: int):
    set_bits = [(byte // (2 ** bit)) % 2 for bit in range(8)]
    return set_bits


server_ip, port = "127.0.0.1", 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, port))

msg = s.recv(1024)
print(f"{msg = }{type(msg) =}")
print(msg.decode())

s.send(add_control_byte("Hello".encode(), b"0xff"))
s.send(add_control_byte("Hello".encode(), b"0x00"))
s.send(add_control_byte("Hello".encode(), b"0x0"))
s.send(add_control_byte("Hello".encode(), b"0b00001"))
s.send(add_control_byte("Hello".encode(), b"0b10"))
s.send(add_control_byte("Hello".encode(), b"0b11"))
