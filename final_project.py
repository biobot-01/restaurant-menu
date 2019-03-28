#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    return "Show all restaurant names"


@app.route('/restaurant/new')
def new_restaurant():
    return "Create a restaurant"


@app.route('/restaurant/<int:restaurant_id>/edit')
def edit_restaurant(restaurant_id):
    return "Edit restaurant with id {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/delete')
def delete_restaurant(restaurant_id):
    return "Delete restaurant with id {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def show_restaurant_menu(restaurant_id):
    return "Show a restaurant menu"


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def new_menu_item(restaurant_id):
    return "Create a menu item for restaurant with id {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    return "Edit menu item with id {} for restaurant with id {}".format(
        menu_id,
        restaurant_id
    )


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def delete_menu_item(restaurant_id, menu_id):
    return "Delete menu item with id {} for restaurant with id {}".format(
        menu_id,
        restaurant_id
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
