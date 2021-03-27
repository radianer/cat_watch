import socket
import threading
import socketserver
import struct
import pickle
import cv2 as cv

class Server:

    def __init__(self, input_port, output_port, hostname = "192.168.178.32"):
        self.input_port = input_port
        self.output_port = output_port
        self.input_server = None
        self.output_server = None
        self.hostname = hostname
        self.running = True
        
        self.input_serve_th = None
        self.output_serve_th = None

    def start(self):
        print("Server started")
        self.input_server = socketserver.TCPServer((self.hostname, self.input_port), TCPInputHandler)
        self.input_server.timeout = 15
        self.output_server = socketserver.TCPServer((self.hostname, self.output_port), TCPOutputHandler)
        self.input_serve_th = threading.Thread(target=self.input_server.serve_forever)
        self.output_serve_th = threading.Thread(target=self.output_server.serve_forever)
        for t in self.input_serve_th, self.output_serve_th: t.start()
        for t in self.input_serve_th, self.output_serve_th: t.join()
        

class TCPInputHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Get Input connection")
        data = b""
        payload_size = struct.calcsize(">L")
        while True:
            while len(data) < payload_size:
                # data = self.request.recv(4096)
                pay_data = self.request.recv(4096)
                if pay_data is None:
                    break
                data += pay_data
            
            print("Done Recv: {}".format(len(data)))

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("msg_size: {}".format(msg_size))
            while len(data) < msg_size:
                # data = self.request.recv(4096)
                msg_data = self.request.recv(4096)
                if msg_data is None:
                    break
                data += msg_data

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv.imdecode(frame, cv.IMREAD_COLOR)
            cv.imshow("Frame", frame)
            cv.waitKey(1)
        
        print("End connection")
    
    def finish(self):
        print("Finish")



class TCPOutputHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Get Output connection")
