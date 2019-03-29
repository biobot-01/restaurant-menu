#!/usr/bin/env python3

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    no_restaurants_msg = None

    if not restaurants:
        no_restaurants_msg = "There are no restaurants listed yet. Add one!"

    return render_template(
        'restaurants.html',
        restaurants=restaurants,
        no_restaurants_msg=no_restaurants_msg
    )


@app.route('/restaurant/new')
def new_restaurant():
    return render_template('new-restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit')
def edit_restaurant(restaurant_id):
    return render_template('edit-restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete')
def delete_restaurant(restaurant_id):
    return render_template(
        'delete-restaurant.html',
        restaurant=restaurant
    )


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def show_restaurant_menu(restaurant_id):
    no_items_msg = None

    if not items:
        no_items_msg = "There are no items on this menu yet. Add some!"

    return render_template(
        'menu.html',
        restaurant=restaurant,
        items=items,
        no_items_msg=no_items_msg
    )


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def new_menu_item(restaurant_id):
    return render_template('new-menu-item.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    return render_template(
        'edit-menu-item.html',
        restaurant=restaurant,
        item=item
    )


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def delete_menu_item(restaurant_id, menu_id):
    return render_template(
        'delete-menu-item.html',
        restaurant=restaurant,
        item=item
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
