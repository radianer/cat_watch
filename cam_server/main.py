# from server_tcp import Server
from server_http import Server
from image_processor import ImageProcessor

input_port = 5000
output_port = 9091

if __name__ == "__main__":
    server = Server(input_port)
    server.start()
    processor = ImageProcessor(server)
    processor.display_images()