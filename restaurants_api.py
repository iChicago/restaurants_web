from flask import Flask, jsonify, redirect, url_for, render_template, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
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
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/json')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(menu_items=[item.serialize for item in items])


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/json')
def restaurant_one_menu_json(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menu_items=[item.serialize])

# New menu items
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    # we use (request) to get data from the form.
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['form_name'],
                            description=request.form['form_description'],
                            price=request.form['form_price'],
                            course=request.form['form_course'],
                            restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("New menu item ({0}) was created".format(new_item.name))
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    edited_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['form_name']:
            edited_item.name = request.form['form_name']
        if request.form['form_description']:
            edited_item.description = request.form['form_description']
        if request.form['form_price']:
            edited_item.price = request.form['form_price']
        if request.form['form_course']:
            edited_item.course = request.form['form_course']
        session.add(edited_item)
        session.commit()
        flash("Menu item ({0}) was edited".format(edited_item.name))
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'edit_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=edited_item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash("Menu item ({0}) was deleted".format(item_to_delete.name))
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'delete_menu_item.html', item=item_to_delete)


if __name__ == '__main__':
    # Reload if there is a change, Display debug messages
    app.debug = True
    # Put mor secure key fo real app
    app.secret_key = 'mySecretKey'
    app.run(host='0.0.0.0', port=5000)
