import socket
import struct

dummy_data_one = 3.0
dummy_data_two = 23.4
HOST = '172.31.15.89'
PORT = 8080

def retrieve_file_data(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

file = retrieve_file_data("test.wav")
file_length = len(file)
data_package = struct.pack("!Idd", file_length, dummy_data_one, dummy_data_two)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    print("connecting")
    conn.connect((HOST, PORT))
    conn.sendall(data_package)
    conn.sendall(file)
    conn.shutdown(socket.SHUT_WR)
