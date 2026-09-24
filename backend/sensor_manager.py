# sensor_manager.py
# The sensor_manager is expected to keep a list of, and take input from all active sensors
# It will buffer input from all sensors, and distribute it amongst other files on request
# The sensor_manager will also carry the logic for adding sensors to the network

import queue
import socket
import struct

# debug test function, move this to a utility file later for reusability
def write_data(file, content_string):
    if file:
        file.write(content_string)

# Testing TCP connection between WSL and host machine
HOST = ''
PORT = 8080
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("Listening")
    while True:
        conn, addr = s.accept()

        print('Connected from ', addr)
        header = conn.recv(struct.calcsize("!Idd"))
        file_length, dum1, dum2 = struct.unpack("!Idd", header)
        print(dum1)
        print(dum2)

        received_data = b''
        while len(received_data) < file_length:
            chunk = conn.recv(min(4096, file_length - len(received_data)))
            if not chunk:
                break
            received_data += chunk

        with open("test.wav", "wb") as f:
            write_data(f, received_data)
    



