#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler


def main():
    try:
        port = 8000
        server_address = ('', port)
        httpd = HTTPServer(server_address, WebServerHandler)
        print("Web server running on port {}".format(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        httpd.socket.close()


if __name__ == '__main__':
    main()
