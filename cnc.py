#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json
import subprocess
from typing import ByteString
from zlib import decompress
from base64 import encodebytes, decodebytes
from io import BytesIO

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Using https://blog.anvileight.com/posts/simple-python-http-server/ as a starting point to handle requests from implant"""
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, lol')

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

    serv.serve_forever()
    

if __name__ == "__main__":
    main()