from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CItem

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# The main page without any Login
@app.route('/')
def mainPage():
    catalogs = session.query(Catalog).all()
    return render_template('home.html', catalogs=catalogs)


# The Page of items of a specific catalog
@app.route('/catalog/<string:catalog_name>/items')
def catalogItems(catalog_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    items = session.query(CItem).filter_by(catalog_id=catalog.id).all()
    num = session.query(CItem).filter_by(catalog_id=catalog.id).count()
    return render_template('items.html', catalog_name=catalog_name, num=num, items=items)


# The Page of specific item of a specific catalog
@app.route('/catalog/<string:catalog_name>/<string:item_name>')
def itemDesc(catalog_name, item_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    item = session.query(CItem).filter_by(catalog_id=catalog.id).filter_by(name=item_name).one()
    return render_template('item.html', item=item)


# The Page of Creating new Item
@app.route('/catalog/new', methods=['GET', 'POST'])
def addItem():
    catalogs = session.query(Catalog).all()
    if request.method == 'POST':
        cat = session.query(Catalog).filter_by(name=request.form['sel']).one()
        newitem = CItem(name=request.form['name'], description=request.form['desc'], catalog=cat,
                           catalog_id=cat.id)
        session.add(newitem)
        session.commit()
        flash("Item has been Added")
        return redirect(url_for('mainPage'))
    else:
        return render_template('new.html', catalogs=catalogs)


# The Page of Editing specific item in a catalog
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    catalogs = session.query(Catalog).all()
    item = session.query(CItem).filter_by(name=item_name).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['desc']
        newcat = request.form['sel']
        item.catalog = session.query(Catalog).filter_by(name=newcat).one()
        session.add(item)
        session.commit()
        flash("Item has been edited")
        return redirect(url_for('mainPage'))
    else:
        return render_template('edit.html', item=item, catalogs=catalogs)


# The Page of deleting a specific item of a specific catalog
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    item = session.query(CItem).filter_by(name=item_name).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item has been deleted")
        return redirect(url_for('mainPage'))
    else:
        return render_template('delete.html', item=item)


# The API response to Get request from user
@app.route('/catalog.json')
def getJson():
    catalogs = session.query(Catalog).all()
    res = []
    for i in catalogs:
        items = session.query(CItem).filter_by(catalog_id=i.id).all()
        temp = {'Item': [j.serialize for j in items],
                'name': i.name,
                'id': i.id,
                }
        res.append(temp)
    return jsonify(Category=res)

#Login method


if __name__ == '__main__':
    app.secret_key = '12345'
    app.debug = True
app.run(host='0.0.0.0', port=8080)
