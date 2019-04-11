#!/usr/bin/env python3

import json
import random
import string

from flask import (
    Flask, render_template, request, redirect, url_for, jsonify, flash,
    session as login_session, make_response
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import requests

from database_setup import Base, User, Restaurant, MenuItem

client_secret_file = 'client_secrets.json'

with open(client_secret_file, 'r') as f:
    web_client_id = json.load(f)['web']['client_id']

client_id = web_client_id

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu_with_users.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    restaurants = session.query(Restaurant).all()
    no_restaurants_msg = None

    if not restaurants:
        no_restaurants_msg = 'There are no restaurants listed yet. Add one!'

    if 'username' not in login_session:
        return render_template(
            'public-restaurants.html',
            restaurants=restaurants,
            no_restaurants_msg=no_restaurants_msg,
        )
    else:
        return render_template(
            'restaurants.html',
            restaurants=restaurants,
            no_restaurants_msg=no_restaurants_msg,
        )


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    # Check if user is signed in
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        user_id = login_session['user_id']

        if name:
            new_restaurant = Restaurant(
                name=name,
                user_id=user_id,
            )

            session.add(new_restaurant)
            session.commit()

            flash('New Restaurant Created')

            return redirect(url_for('show_restaurants'))

    return render_template('new-restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    edit_restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id,
    ).one()

    # Check if user is signed in
    if 'username' not in login_session:
        return redirect('/login')

    if edit_restaurant.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to edit this restaurant. "
                "Please create your own restaurant in order "
                "to edit.');}</script><body onload='myFunction()''>")

    if request.method == 'POST':
        name = request.form['name']

        if name:
            edit_restaurant.name = name

            flash('Restaurant Successfully Edited')

            return redirect(url_for('show_restaurants'))

    return render_template('edit-restaurant.html', restaurant=edit_restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    delete_restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id,
    ).one()

    # Check if user is signed in
    if 'username' not in login_session:
        return redirect('/login')

    if delete_restaurant.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to delete this restaurant. "
                "Please create your own restaurant in order "
                "to delete.');}</script><body onload='myFunction()''>")

    if request.method == 'POST':
        session.delete(delete_restaurant)
        session.commit()

        flash('Restaurant Successfully Deleted')

        return redirect(url_for('show_restaurants'))

    return render_template(
        'delete-restaurant.html',
        restaurant=delete_restaurant,
    )


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = get_user_info(restaurant.user_id)
    menu_items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id,
    ).all()
    no_menu_items_msg = None

    if not menu_items:
        no_menu_items_msg = 'There are no items on this menu yet. Add some!'

    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        return render_template(
            'public-menu.html',
            restaurant=restaurant,
            creator=creator,
            items=menu_items,
            no_items_msg=no_menu_items_msg,
        )
    else:
        return render_template(
            'menu.html',
            restaurant=restaurant,
            creator=creator,
            items=menu_items,
            no_items_msg=no_menu_items_msg,
        )


@app.route(
    '/restaurant/<int:restaurant_id>/menu/new',
    methods=['GET', 'POST'],
)
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    # Check if user is signed in
    if 'username' not in login_session:
        return redirect('/login')

    if login_session['user_id'] != restaurant.user_id:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to add menu items to this restaurant. "
                "Please create your own restaurant in order "
                "to add items.');}</script><body onload='myFunction()''>")

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
            restaurant_id=restaurant_id,
            user_id=restaurant.user_id,
        )

        session.add(new_item)
        session.commit()

        flash('Menu Item Created')

        return redirect(url_for(
            'show_restaurant_menu',
            restaurant_id=restaurant_id,
        ))

    return render_template('new-menu-item.html', restaurant=restaurant)


@app.route(
    '/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
    methods=['GET', 'POST'],
)
def edit_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    edit_item = session.query(MenuItem).filter_by(
        id=menu_id,
    ).one()

    # Check if user is signed in
    if 'username' not in login_session:
        return redirect('/login')

    if login_session['user_id'] != restaurant.user_id:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to edit menu items to this restaurant. "
                "Please create your own restaurant in order "
                "to edit items.');}</script><body onload='myFunction()''>")

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']

        if name:
            edit_item.name = name

        if description:
            edit_item.description = description

        if price:
            edit_item.price = price

        if course:
            edit_item.course = course

        flash('Menu Item Successfully Edited')

        return redirect(url_for(
            'show_restaurant_menu',
            restaurant_id=restaurant_id,
        ))

    return render_template(
        'edit-menu-item.html',
        restaurant=restaurant,
        item=edit_item,
    )


@app.route(
    '/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
    methods=['GET', 'POST'],
)
def delete_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    delete_item = session.query(MenuItem).filter_by(id=menu_id).one()

    # Check if user is signed in
    if 'username' not in login_session:
        return redirect('/login')

    if login_session['user_id'] != restaurant.user_id:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to delete menu items to this restaurant. "
                "Please create your own restaurant in order "
                "to delete items.');}</script><body onload='myFunction()''>")

    if request.method == 'POST':
        session.delete(delete_item)
        session.commit()

        flash('Menu Item Successfully Deleted')

        return redirect(url_for(
            'show_restaurant_menu',
            restaurant_id=restaurant_id,
        ))

    return render_template(
        'delete-menu-item.html',
        restaurant=restaurant,
        item=delete_item,
    )


@app.route('/login')
def show_login():
    # Create anti-forgery state token
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits
    ) for x in range(32))
    login_session['state'] = state

    return render_template('login.html', CLIENT_ID=client_id, STATE=state)


# Connect with Google login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(
            json.dumps('Invalid state parameter.'),
            401,
        )
        response.headers['Content-type'] = 'application/json'

        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade authorization code into credentials object
        oauth_flow = flow_from_clientsecrets(client_secret_file, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'),
            401,
        )
        response.headers['Content-type'] = 'application/json'

        return response

    # Check access token is valid
    access_token = credentials.access_token
    auth_url = ('https://www.googleapis.com/oauth2/v1/'
                'tokeninfo?access_token={}'.format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(auth_url, 'GET')[1])

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(
            json.dumps(result.get('error')),
            500,
        )
        response.headers['Content-type'] = 'application/json'

        return response

    # Verify access token is used for intended user
    google_id = credentials.id_token['sub']

    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."),
            401,
        )
        response.headers['Content-type'] = 'application/json'

        return response

    # Verify access token is valid for this app
    if result['issued_to'] != client_id:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's ID."),
            401,
        )
        print("Token's client ID doesn't match app's ID.")
        response.headers['Content-type'] = 'application/json'

        return response

    # Check if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')

    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200,
        )
        response.headers['Content-type'] = 'application/json'

        return response

    # Store access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get user info
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {
        'access_token': credentials.access_token,
        'alt': 'json',
    }
    user_request = requests.get(userinfo_url, params=params)
    user_data = user_request.json()

    login_session['username'] = user_data['name']
    login_session['picture'] = user_data['picture']
    login_session['email'] = user_data['email']

    user_id = get_user_id(login_session['email'])

    if not user_id:
        user_id = create_user(login_session)

    login_session['user_id'] = user_id

    output = ('<h1>Welcome, {}!</h1><img src="{}" '
              'style="width: 300px; height: 300px; '
              'border-radius: 50%;">'.format(
                login_session['username'],
                login_session['picture'],
              ))

    flash('You are now logged in as {}'.format(login_session['username']))
    print('Done!')
    return output


# Disconnect Google login - revoke a current user's token and reset
# their login session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'),
            401,
        )
        response.headers['Content-type'] = 'application/json'

        return response

    # Execute HTTP GET response to revoke current token
    disconnect_url = ('https://accounts.google.com/o/oauth2/'
                      'revoke?token={}'.format(access_token))
    h = httplib2.Http()
    result = h.request(disconnect_url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['picture']
        del login_session['email']

        response = make_response(
            json.dumps('Successfully disconnected.'),
            200,
        )
        response.headers['Content-type'] = 'application/json'

        return response
    else:
        # For any reason, the given token was invalid
        response = make_response(
            json.dumps('Failed to revoke token for given user.'),
            400,
        )
        response.headers['Content-type'] = 'application/json'

        return response


def create_user(login_session):
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'],
    )

    session.add(new_user)
    session.commit()

    user = session.query(User).filter_by(
        email=login_session['email'],
    ).one()

    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()

    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()

        return user.id
    except Exception:
        return None


# JSON API Routes
@app.route('/restaurants/JSON')
def restaurants_json():
    restaurants = session.query(Restaurant).all()

    return jsonify(
        restaurants=[r.serialize for r in restaurants]
    )


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    menu_items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id,
    ).all()

    return jsonify(items=[i.serialize for i in menu_items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()

    return jsonify(item=menu_item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000, threaded=False)
