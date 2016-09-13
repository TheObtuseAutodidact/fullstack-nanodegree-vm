from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import pdb

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#  Making a API Endpoint (GET)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).get(restaurant_id)
    items = session.query(MenuItem).filter_by(
        restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(item.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    # return "Hello, World!"
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)
    # output = ''
    # # pdb.set_trace()
    # for i in items:
    #     output += i.name + "</br>"
    #     output += i.price + "</br>"
    #     output += i.description + "</br>"
    #     output += '</br>'
    # return output

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        # pdb.set_trace()
        newItem = MenuItem(name=request.form['name'],
            restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/',
    methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).get(restaurant_id)
    editItem = session.query(MenuItem).get(menu_id)
    if request.method == 'POST':
        if request.form['name']:
            editItem.name=request.form['name']
        session.add(editItem) # do i need this?
        session.commit()
        flash("Menu item edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant=restaurant,
            editItem=editItem, menu_id=menu_id)

    # return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
    methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    doomedItem = session.query(MenuItem).get(menu_id)
    if request.method == 'POST':
        session.delete(doomedItem)
        session.commit()
        flash("%s has been deleted from the menu!" % doomedItem.name)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id,
            item=doomedItem))
    else:
        return render_template('deletemenuitem.html',
            restaurant_id=restaurant_id, menu_id=menu_id, item=doomedItem)
    # return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.secret_key = 'my secret key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
