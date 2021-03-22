from server import Server

input_port = 8080
output_port = 8081

if __name__ == "__main__":
    server = Server(input_port, output_port)
    server.start()