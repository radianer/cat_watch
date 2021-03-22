import socket
import threading
import socketserver

class Server:

    def __init__(self, input_port, output_port):
        self.input_port = input_port
        self.output_port = output_port
        self.input_server = None
        self.output_server = None
        self.hostname = socket.gethostname()
        self.running = True

    def start(self):
        print("Server started")
        self.input_server = socketserver.TCPServer((self.hostname, self.input_port), TCPInputHandler)
        self.output_server = socketserver.TCPServer((self.hostname, self.output_port), TCPOutputHandler)
        self.input_server.serve
        

class TCPInputHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Get Input connection")


class TCPOutputHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Get Output connection")
