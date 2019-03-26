#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for

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

        return redirect(url_for(
            'restaurant_menu',
            restaurant_id=restaurant_id
        ))
    else:
        return render_template(
            'new-menu-item.html',
            restaurant_id=restaurant_id
        )


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def delete_menu_item(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
