#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler


class WebServerHandler(BaseHTTPRequestHandler):
    """The HTTP method this web server can handle"""

    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = '''
                    <html>
                      <head>
                        <title>Hello</title>
                      </head>
                      <body>
                        <h1>Hello!</h1>
                      </body>
                    </html>
                '''

                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = '''
                    <html>
                      <head>
                        <title>Hola</title>
                      </head>
                      <body>
                        <h1>&#161Hola</h1>
                        <a href="/hello">Back to Hello</a>
                      </body>
                    </html>
                '''

                self.wfile.write(output.encode())
                print(output)
                return
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))


def main():
    """Main function for this file is to create a web server instance"""

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
