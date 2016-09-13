from flask import Flask, render_template, request, flash, redirect, url_for
from flask import jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import pdb

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
#
# # restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
#
#
# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


app = Flask(__name__)

@app.route('/restaurants/') # add the final '/' for url to work with or without the '/' on the end
@app.route('/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/JSON')
def showRestaurantsJSONi():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurants])

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        flash(new_restaurant.name + " Created!")
        return redirect(url_for('showRestaurants'))
    else:
      return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # return render_template('editrestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)
    restaurant = session.query(Restaurant).get(restaurant_id)
    if request.method == 'POST':
        restaurant.name = request.form['name']
        # pdb.set_trace()
        session.add(restaurant)
        session.commit()
        flash(restaurant.name + " Successfully Edited")
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('editRestaurant.html', restaurant=restaurant)



@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).get(restaurant_id)
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash(restaurant.name + " Successfully Deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant_id=restaurant.id, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    restaurant = session.query(Restaurant).get(restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    restaurant = session.query(Restaurant).get(restaurant_id)
    return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).get(menu_id)
    return jsonify(MenuItem=item.serialize)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        menu_item = MenuItem(name=request.form['name'],
                             course=request.form['course'],
                             price=request.form['price'],
                             description=request.form['description'],
                             restaurant_id=restaurant_id)
        session.add(menu_item)
        session.commit()
        flash(menu_item.name + " Added To Menu!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))

    return render_template('newmenu.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).get(restaurant_id)
    item = session.query(MenuItem).get(menu_id)
    if request.method =='POST':
        item.name=request.form['name']
        item.course=request.form['course']
        item.price = request.form['price']
        item.description = request.form['description']
        session.commit()
        flash(item.name + " Successfully Edited")
        return redirect(url_for('.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenu.html', restaurant=restaurant,
            menu_id=menu_id, item=item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).get(restaurant_id)
    item = session.query(MenuItem).get(menu_id)
    if request.method == 'POST':
        session.delete(item)
        flash("{{ item.name }} has been removed from {{ restaurant.name }}'s menu.'")
        return redirect(url_for('.showMenu', restaurant_id=restaurant_id))
    return render_template('deletemenu.html', restaurant=restaurant,
        menu_id=menu_id, item=item)


if __name__ == '__main__':
    app.secret_key = 'my_secret'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
