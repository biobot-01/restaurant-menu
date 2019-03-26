#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import parse_qs

from database_setup import Base, Restaurant, MenuItem

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

# Database to connect
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind database to session
Base.metadata.bind = engine
# Create the session
Session = sessionmaker(bind=engine)
session = Session()


class WebServerHandler(BaseHTTPRequestHandler):
    """The HTTP method this web server can handle"""

    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                # Query database and fetch all the restaurant names
                restaurants = session.query(Restaurant).all()
                # Send 200 OK response
                self.send_response(200)
                # Send headers
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                # Main page layoout
                html = '''<!doctype html>
                    <html>
                      <head>
                        <meta charset="utf-8">
                        <title>Restaurant Names</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                      </head>
                      <body>
                          <h1>Restaurant Names</h1>
                          <a href="/restaurants/new">Add a new Restaurant</a>
                          <br>
                          <ul>
                            {restaurant_names}
                          </ul>
                      </body>
                    </html>
                '''

                # Single restaurant entry html template
                restaurant_name_content = '''<li>{restaurant_name}<br>
                    <a href="#">edit</a>
                    <a href="#">delete</a></li>
                '''

                def create_restaurant_names_content(restaurants):
                    """Return the names of restaurants with html template"""

                    content = ''

                    for restaurant in restaurants:
                        content += restaurant_name_content.format(
                            restaurant_name=restaurant.name
                        )

                    return content

                rendered_content = html.format(
                    restaurant_names=create_restaurant_names_content(
                        restaurants
                    )
                )

                # Send the response
                self.wfile.write(rendered_content.encode())
                # Print out response for debugging
                print(rendered_content)
                return

            if self.path.endswith('/restaurants/new'):
                # Send 200 OK response
                self.send_response(200)
                # Send headers
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                # Main page layoout
                html = '''<!doctype html>
                    <html>
                      <head>
                        <meta charset="utf-8">
                        <title>Add New Restaurant</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                      </head>
                      <body>
                          <h1>Add New Restaurant</h1>
                          <a href="/restaurants">Go back</a>
                          <br><br>
                          <form action="/restaurants/new" method="POST">
                            <label for="restaurantName">Restaurant Name</label>
                            <input type="text" name="restaurantName" placeholder="New Restaurant Name">
                            <button type="submit">Create</button>
                          </form>
                      </body>
                    </html>
                '''

                # Send the response
                self.wfile.write(html.encode())
                # Print out response for debugging
                print(html)
                return

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                # Get length of data
                length = int(self.headers.get('Content-length', 0))
                # Read the correct amount of data from request
                data = self.rfile.read(length).decode()
                # Extract the "restaurantName" field from request data
                restaurant_name = parse_qs(data)["restaurantName"][0]
                # Escape HTML tags in data for security
                restaurant_name = restaurant_name.replace("<", "&lt;")
                # Create new Restaurant object and store data in database
                new_restaurant = Restaurant(name=restaurant_name)
                session.add(new_restaurant)
                session.commit()

                # Send a 303 redirect back response (to restaurants page)
                self.send_response(303)
                # Send headers
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Location', '/restaurants')
                self.end_headers()

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
