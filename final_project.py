#!/usr/bin/env python3

from flask import Flask, render_template

app = Flask(__name__)

# Add fake variables for testing
# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [
    {'name': 'The CRUDdy Crab', 'id': '1'},
    {'name': 'Blue Burgers', 'id': '2'},
    {'name': 'Taco Hut', 'id': '3'}
]

# Fake Menu Items
items = [
    {
        'name': 'Cheese Pizza',
        'description': 'made with fresh cheese',
        'price': '$5.99',
        'course': 'Entree',
        'id': '1'
    },
    {
        'name': 'Chocolate Cake',
        'description': 'made with Dutch Chocolate',
        'price': '$3.99',
        'course': 'Dessert',
        'id': '2'
    },
    {
        'name': 'Caesar Salad',
        'description': 'with fresh organic vegetables',
        'price': '$5.99',
        'course': 'Entree',
        'id': '3'
    },
    {
        'name': 'Iced Tea',
        'description': 'with lemon',
        'price': '$.99',
        'course': 'Beverage',
        'id': '4'
    },
    {
        'name': 'Spinach Dip',
        'description': 'creamy dip with fresh spinach',
        'price': '$1.99',
        'course': 'Appetizer',
        'id': '5'
    }
]

item = {
    'name': 'Cheese Pizza',
    'description': 'made with fresh cheese',
    'price': '$5.99',
    'course': 'Entree'
}


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    # restaurants = []
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
