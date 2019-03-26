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
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id
    ).one()
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


@app.route('/restaurant/<int:restaurant_id>/new')
def new_menu_item(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def delete_menu_item(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
