from server import Server

input_port = 9090
output_port = 9091

if __name__ == "__main__":
    server = Server(input_port, output_port)
    server.start()