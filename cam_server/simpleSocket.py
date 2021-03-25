import socket
import sys

HOST = ""
PORT = 9090
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

s.bind((HOST, PORT))
print("Socket bind complete")

s.listen(10)
print("socket now listening")

conn, addr = s.accept()

while True:
    data = conn.recv(80)
    print(sys.getsizeof(data))
    
