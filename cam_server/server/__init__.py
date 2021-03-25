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
        
        self.input_serve_th = None
        self.output_serve_th = None

    def start(self):
        print("Server started")
        self.input_server = socketserver.TCPServer((self.hostname, self.input_port), TCPInputHandler)
        self.output_server = socketserver.TCPServer((self.hostname, self.output_port), TCPOutputHandler)
        self.input_serve_th = threading.Thread(target=self.input_server.serve_forever)
        self.output_serve_th = threading.Thread(target=self.output_server.serve_forever)
        for t in self.input_serve_th, self.output_serve_th: t.start()
        for t in self.input_serve_th, self.output_serve_th: t.join()
        

class TCPInputHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Get Input connection")


class TCPOutputHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Get Output connection")
