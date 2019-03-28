#!/usr/bin/env python3

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new')
def new_restaurant():
    return render_template('new-restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit')
def edit_restaurant(restaurant_id):
    return render_template('edit-restaurant.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/delete')
def delete_restaurant(restaurant_id):
    return render_template(
        'delete-restaurant.html',
        restaurant_id=restaurant_id
    )


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def show_restaurant_menu(restaurant_id):
    return render_template('menu.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def new_menu_item(restaurant_id):
    return render_template('new-menu-item.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    return render_template(
        'edit-menu-item.html',
        restaurant_id=restaurant_id,
        menu_id=menu_id
    )


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def delete_menu_item(restaurant_id, menu_id):
    return render_template(
        'delete-menu-item.html',
        restaurant_id=restaurant_id,
        menu_id=menu_id
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
