import sqlite3 
from flask import Flask, request, render_template, redirect, url_for, session, flash, g, abort


MyApp = Flask(__name__)
DATABASE = 'database.db'
MyApp.secret_key = '12308adsijkadsads129033210321'

@MyApp.route('/')
def index():
  return render_template('index.html')

@MyApp.route('/dashboard')
def dashboard():
  if(isLoggedIn()):
    return render_template('dashboard.html')
  else:
    abort(418)

@MyApp.route('/loginpage')
def loginpage():
  return render_template('login.html')

@MyApp.route('/page3')
def page3():
  if(isLoggedIn()):
    return render_template('page3.html')
  else:
    abort(418)

@MyApp.route('/page4')
def page4():
  if(isLoggedIn()):
    return render_template('page4.html')
  else:
    abort(418)

@MyApp.route('/page5')
def page5():
  if(isLoggedIn()):
    return render_template('page5.html')
  else:
    abort(418)

@MyApp.route('/logoutpage')
def logoutpage():
  session.pop('login', None)
  return redirect("/")

@MyApp.route('/login', methods=['POST'])
def login():
  password = str(request.form['psw'])
  username = str(request.form['uname'])

  user_exists = query_db('SELECT COUNT(*) FROM USERS WHERE username = ?', [username])

  if(user_exists[0][0] == 1):
    password_true = query_db('SELECT COUNT(*) FROM USERS WHERE username = ? AND password = ?', (username, password))
    if(password_true[0][0] == 1):
      session['login'] = "username"
      return redirect("/dashboard")
    else:
      flash('Login failed.')
      return render_template('login.html')
  else:
      flash('Login failed.')
      return render_template('login.html')

@MyApp.errorhandler(418)
def foureighteen(e):
  return render_template('418.html'), 418

@MyApp.errorhandler(404)
def foureighteen(e):
  return render_template('418.html'), 404
#-----------------------------------------------------------------
# connection_to_sqlite_database as the name implies handles our
# connection to the SQLITE database.db database file. We keep
# the connection open until our database commits/reads have 
# fully completed. 
# -----------------------------------------------------------------

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
  
def isLoggedIn():
  if(session.get('login') is None):
    return False
  else:
    return True


@MyApp.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
   MyApp.run(host='0.0.0.0', port=80, debug=True)
