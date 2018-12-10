from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession =sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')


def HelloWorld():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    output = '<html><body><ul>'
    for item in items:
        output+= '<li>'+ item.name + '</li>'
    output+= '</ul></body></html>'
    return output


if __name__ == '__main__':
    # Reload if there is a change, Display debug messages
    app.debug = True
    app.run(host= '0.0.0.0', port= 5000)
