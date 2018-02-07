from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import orm_db

app = Flask(__name__)


@app.route('/')
@app.route('/restaurant')
def restaurantHome():
    return render_template('menu.html', items = orm_db.getData('restaurant'), restaurant = orm_db.getData('restaurant')[0])


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    return render_template('menuById.html', items = orm_db.getDataById(idd = restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/JSON')
def restaurantMenuJSON(restaurant_id):
    return orm_db.getJsonData(idd = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        orm_db.createData('menuitem',request.form['name'],restaurant_id)
        flash('new item just added')
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        orm_db.updateData('menuitem', menu_id, request.form['name'])
        flash('item was updated')
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('edit.html', item = orm_db.getOneData(idNumber = menu_id, idRes = restaurant_id))

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        orm_db.delData(idNumber = menu_id, idRes = restaurant_id)
        flash('item was deleted')
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', item = orm_db.getOneData(idNumber = menu_id, idRes = restaurant_id))



if __name__ == '__main__':
    app.secret_key = 'password'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
