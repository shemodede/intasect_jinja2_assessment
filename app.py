from turtle import title
from flask import Flask, request, render_template, request, url_for, redirect, g
from datetime import datetime
import sqlite3
from sql import functions

DB_FILENAME = "database.sqlite"

app = Flask(__name__)

class UserAuth:
    userid = None
    user_authenticated = False
    name = ''
    email = ''
    loginid = None

user_auth = UserAuth()

def authenticate_user(loginid, password):
    user_obj = functions.get_user_object(DB_FILENAME, loginid, password)
    
    if user_obj is not None and len(user_obj) > 1:
        user_auth.userid = user_obj[0]
        user_auth.name = user_obj[1]
        user_auth.email = user_obj[2]
        user_auth.loginid = user_obj[3]
        user_auth.user_authenticated = True
        g.is_auth = True
    return user_obj

def is_authenticated():
    if not user_auth.user_authenticated:
        return redirect(url_for('login'))

@app.route('/')
def index():
    functions.create_db(DB_FILENAME)
    functions.create_tables(DB_FILENAME)
    return render_template('index.html')

@app.route('/user_profile', methods=['POST', 'GET'])
def user_profile():
    context = {}
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        loginid = request.form['loginid']
        functions.update_user_profile(DB_FILENAME, name, email, password, loginid, user_auth.userid)
        return redirect(url_for('user_profile'))
    if request.method == 'GET':
        user_object = functions.get_user_object_with_id(DB_FILENAME, user_auth.userid)
        if user_object is None:
            pass
        else:
            name = user_object[1]
            email = user_object[2]
            password = user_object[3]
            loginid = user_object[4]
            context = {
                'name': name,
                'email': email,
                'password': password,
                'loginid': loginid
            }
    return render_template('user_profile.html', **context)

@app.route('/tyre_duration', methods=['POST', 'GET'])
def tyre_duration():
    context = {}
    if request.method == 'GET':
        context['tyre_journey_data'] = functions.get_tyre_journey_data(DB_FILENAME)
    return render_template('tyre_duration.html', **context)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        loginid = request.form['loginid']
        password = request.form['password']
        authenticate_user(loginid, password)
        return redirect(url_for('user_profile'))
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        loginid = request.form['loginid']
        passwd = request.form['password']
        usertype = 1
        functions.insert_user_data(DB_FILENAME, name, email, loginid, passwd, usertype)
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/chassis_types', methods=['POST', 'GET'])
def chassis_types():
    context = {}
    if request.method == 'POST':
        name = request.form['name']
        functions.insert_chassis_type_data(DB_FILENAME, name)
        return redirect(url_for('chassis_types'))
    if request.method == 'GET':
        context['chassis_data'] = functions.select_chassis_type_data(DB_FILENAME)
    return render_template('chassis_types.html', **context)

@app.route('/vehicles', methods=['POST', 'GET'])
def vehicles():
    context = {}
    if request.method == 'POST':
        fleet_code = request.form['fleet_code']
        regnumber = request.form['regnumber']
        chassisid = request.form['chassisid']
        functions.insert_vehicle_data(DB_FILENAME, fleet_code, regnumber, chassisid)
        return redirect(url_for('vehicles'))
    if request.method == 'GET':
        context['chassis_data'] = functions.select_chassis_type_data(DB_FILENAME)
        context['vehicle_data'] = functions.select_vehicle_data(DB_FILENAME)
    return render_template('vehicles.html', **context)

@app.route('/tyres', methods=['POST', 'GET'])
def tyres():
    context = {}
    if request.method == 'POST':
        name = request.form['name']
        serialnum = request.form['serialnum']
        functions.insert_tyre_data(DB_FILENAME, name, serialnum)
        return redirect(url_for('tyres'))
    if request.method == 'GET':
        context['tyre_data'] = functions.select_tyre_data(DB_FILENAME)
    return render_template('tyres.html', **context)

@app.route('/tyre_location', methods=['POST', 'GET'])
def tyre_location():
    context = {}
    if request.method == 'POST':
        tyreid = request.form['tyreid']
        dateticks = request.form['dateticks']
        direction = request.form['direction']
        vehicleid = request.form['vehicleid']
        print(dateticks)
        dateticks = datetime.strptime(dateticks, "%Y-%m-%d")
        dateticks = (dateticks-datetime.fromtimestamp(0)).total_seconds()
        functions.insert_tyre_location_data(DB_FILENAME, tyreid, dateticks, direction, vehicleid)
        return redirect(url_for('tyre_location'))
    if request.method == 'GET':
        context['tyre_data'] = functions.select_tyre_data(DB_FILENAME)
        context['vehicle_data'] = functions.select_vehicle_data(DB_FILENAME)
        context['tyre_location_data'] = functions.select_tyre_location_data(DB_FILENAME)
    return render_template('tyre_location.html', **context)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.template_filter()
def format_date(date_):
    return datetime.fromtimestamp(date_).strftime("%Y-%m-%d")