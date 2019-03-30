#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
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
    restaurants = session.query(Restaurant).all()
    no_restaurants_msg = None

    if not restaurants:
        no_restaurants_msg = "There are no restaurants listed yet. Add one!"

    return render_template(
        'restaurants.html',
        restaurants=restaurants,
        no_restaurants_msg=no_restaurants_msg
    )


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        name = request.form['name']
        new_restaurant = Restaurant(name=name)

        session.add(new_restaurant)
        session.commit()

        return redirect(url_for('show_restaurants'))

    return render_template('new-restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    edit_restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id
    ).one()

    if request.method == 'POST':
        if request.form['name']:
            edit_restaurant.name = request.form['name']

            return redirect(url_for('show_restaurants'))

    return render_template('edit-restaurant.html', restaurant=edit_restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    delete_restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id
    ).one()

    if request.method == 'POST':
        session.delete(delete_restaurant)
        session.commit()

        return redirect(url_for('show_restaurants'))

    return render_template(
        'delete-restaurant.html',
        restaurant=delete_restaurant
    )


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def show_restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id
    ).all()
    no_menu_items_msg = None

    if not menu_items:
        no_menu_items_msg = "There are no items on this menu yet. Add some!"

    return render_template(
        'menu.html',
        restaurant=restaurant,
        items=menu_items,
        no_items_msg=no_menu_items_msg
    )


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        new_item = MenuItem(
            name=name,
            description=description,
            price=price,
            course=course,
            restaurant_id=restaurant_id
        )

        session.add(new_item)
        session.commit()

        return redirect(url_for(
            'show_restaurant_menu',
            restaurant_id=restaurant_id
        ))

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
