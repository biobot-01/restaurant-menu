#!/usr/bin/env python3

from flask import Flask

from database_setup import Base, Restaurant, MenuItem

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

# Create instance of Flask Class
app = Flask(__name__)

# Database to connect
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind database to session
Base.metadata.bind = engine
# Create the session
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
@app.route('/hello')
def hello_world():
    restaurant = session.query(Restaurant).filter_by(id=2).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant.id
    )
    output = ''

    for item in items:
        output += item.name
        output += '<br>'
        output += item.price
        output += '<br>'
        output += item.description
        output += '<br><br>'

    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
