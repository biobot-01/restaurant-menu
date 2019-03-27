#!/usr/bin/env python3

from flask import (Flask, render_template, request, redirect, url_for,
                   flash, jsonify)

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

# Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id
    ).all()

    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    return jsonify(MenuItem=item.serialize)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id
    ).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id
    ).all()

    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(
            name=request.form['name'],
            restaurant_id=restaurant_id,
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course']
        )
        session.add(new_item)
        session.commit()

        flash("new menu item created!")

        return redirect(url_for(
            'restaurant_menu',
            restaurant_id=restaurant_id
        ))
    else:
        return render_template(
            'new-menu-item.html',
            restaurant_id=restaurant_id
        )


@app.route(
    '/restaurant/<int:restaurant_id>/<int:menu_id>/edit',
    methods=['GET', 'POST']
)
def edit_menu_item(restaurant_id, menu_id):
    edit_item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        if request.form['name']:
            edit_item.name = request.form['name']

        if request.form['description']:
            edit_item.description = request.form['description']

        if request.form['price']:
            edit_item.price = request.form['price']

        if request.form['course']:
            edit_item.course = request.form['course']

        session.add(edit_item)
        session.commit()

        flash("menu item edited!")

        return redirect(url_for(
            'restaurant_menu',
            restaurant_id=restaurant_id
        ))
    else:
        return render_template(
            'edit-menu-item.html',
            item=edit_item
        )


@app.route(
    '/restaurant/<int:restaurant_id>/<int:menu_id>/delete',
    methods=['GET', 'POST']
)
def delete_menu_item(restaurant_id, menu_id):
    delete_item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        session.delete(delete_item)
        session.commit()

        flash("menu item deleted!")

        return redirect(url_for(
            'restaurant_menu',
            restaurant_id=restaurant_id
        ))
    else:
        return render_template(
            'delete-menu-item.html',
            item=delete_item
        )


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
