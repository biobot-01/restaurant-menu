#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import parse_qs

from database_setup import Base, Restaurant, MenuItem

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker


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
                        <br>
                        <form action="/hello" method="POST">
                          <h2><label for="message">What would you like me to say?</label></h2>
                          <br>
                          <input type="text" name="message">
                          <button type="submit">Tell me!</button>
                        </form>
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

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-length', 0))
            data = self.rfile.read(length).decode()
            message = parse_qs(data)['message'][0]
            message = message.replace("<", "&lt;")

            self.send_response(302)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            output = '''<html>
                <head>
                  <title>Form POST</title>
                </head>
                <body>
                  <h1>Okay, how about this:</h1>
                  <h2>{}</h2>
                  <form action="/hello" method="POST">
                    <h3><label for="message">What would you like me to say?</label></h3>
                    <br>
                    <input type="text" name="message">
                    <button type="submit">Tell me!</button>
                  </form>
                </body>
                </html>
            '''
            self.wfile.write(output.format(message).encode())
            print(output.format(message))
        except Exception as e:
            raise e


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
