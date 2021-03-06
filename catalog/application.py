from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CItem

# New imports for this step
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Items"

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# The main page without any Login
@app.route('/')
def mainPage():
    catalogs = session.query(Catalog).all()
    return render_template('home.html', catalogs=catalogs, good=('username' in login_session),
                           google=(login_session['provider'] == 'google'))


# The Page of items of a specific catalog
@app.route('/catalog/<string:catalog_name>/items')
def catalogItems(catalog_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one_or_none()
    items = session.query(CItem).filter_by(catalog_id=catalog.id).all()
    num = session.query(CItem).filter_by(catalog_id=catalog.id).count()
    return render_template('items.html', catalog_name=catalog_name, num=num, items=items)


# The Page of specific item of a specific catalog
@app.route('/catalog/<string:catalog_name>/<string:item_name>')
def itemDesc(catalog_name, item_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one_or_none()
    item = session.query(CItem).filter_by(catalog_id=catalog.id).filter_by(name=item_name).one_or_none()
    return render_template('item.html', item=item, good=('username' in login_session))


# The Page of Creating new Item
@app.route('/catalog/new', methods=['GET', 'POST'])
def addItem():
    if 'username' in login_session :
        catalogs = session.query(Catalog).all()
        if request.method == 'POST':
            cat = session.query(Catalog).filter_by(name=request.form['sel']).one_or_none()
            newitem = CItem(name=request.form['name'], description=request.form['desc'], catalog=cat,
                            catalog_id=cat.id)
            session.add(newitem)
            session.commit()
            flash("Item has been Added")
            return redirect(url_for('mainPage'))
        else:
            return render_template('new.html', catalogs=catalogs)
    else:
        return redirect(url_for('mainPage'))


# The Page of Editing specific item in a catalog
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    if 'username' in login_session:
        catalogs = session.query(Catalog).all()
        item = session.query(CItem).filter_by(name=item_name).one_or_none()
        if request.method == 'POST':
            item.name = request.form['name']
            item.description = request.form['desc']
            newcat = request.form['sel']
            item.catalog = session.query(Catalog).filter_by(name=newcat).one_or_none()
            session.add(item)
            session.commit()
            flash("Item has been edited")
            return redirect(url_for('mainPage'))
        else:
            return render_template('edit.html', item=item, catalogs=catalogs)
    else:
        return redirect(url_for('mainPage'))


# The Page of deleting a specific item of a specific catalog
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    if 'username' in login_session:
        item = session.query(CItem).filter_by(name=item_name).one_or_none()
        if request.method == 'POST':
            session.delete(item)
            session.commit()
            flash("Item has been deleted")
            return redirect(url_for('mainPage'))
        else:
            return render_template('delete.html', item=item)
    else:
        return redirect(url_for('mainPage'))

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


# Login methods
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        # print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    #print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        #print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #print 'In gdisconnect access token is %s', access_token
    #print 'User name is: '
    #print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    #print 'result is '
    #print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('gdisconnect'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    #print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    #    user_id = getUserID(login_session['email'])
    #   if not user_id:
    #      user_id = createUser(login_session)
    # login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return redirect(url_for('mainPage'))


if __name__ == '__main__':
    app.secret_key = '12345'
    app.debug = True
app.run(host='0.0.0.0', port=8080)
