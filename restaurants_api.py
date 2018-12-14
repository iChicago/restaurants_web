from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def hello_world():
    """List all restaurants on the home page"""
    restaurants = session.query(Restaurant).all()
    output = '<html><body><h1>Restaurants List</h1>'
    for restaurant in restaurants:
        output = output + '<br>' + restaurant.name + '<br>'
    output = output + '</body></html>'
    return output


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    output = '<html><body><h1>' + restaurant.name + '</h1>'
    for item in items:
        output += '<br>' + item.name + '<br>' + item.price + '<br>' + item.description + '<br>'
    output += '</body></html>'
    return output


@app.route('/restaurants/<int:restaurant_id>/new')
def new_menu_item(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def delete_menu_item(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    # Reload if there is a change, Display debug messages
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
