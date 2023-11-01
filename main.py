import os
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, session
import secrets

# Generates a random URL-safe string of 24 characters


app = Flask(__name__)

load_dotenv()

# retrieve MongoDB link from environment variable
MONGO_DB_LINK = os.getenv("MONGO_DB_LINK")
password = str(os.getenv("PASSWORD"))

# create MongoClient instance
client = MongoClient(MONGO_DB_LINK)

# create or retrieve database
db = client["firstcome"]
orders = db['Orders']
carts = db['Carts']
sessions = db['Sessions']

app = Flask(__name__)
secret_key = secrets.token_urlsafe(24)
app.secret_key = secret_key


# Database Functions


## DASHBOARD CODE ###

def get_order_data():
    return list(orders.find())


def update_status(order_id, new_status):
    order = orders.find_one({'_id': ObjectId(order_id)})
    current_status = order['Status']
    delivery_method = order['DeliveryMethod']

    status_sequence = ['Not Started', 'Preparation', 'Cooking',
                       'Take Out', 'Out for Delivery', 'Done']
    current_index = status_sequence.index(current_status)
    next_index = (current_index + 1) % len(status_sequence)
    new_status = status_sequence[next_index]

    if current_index == 3:
        if delivery_method == 'Take Out':
            new_status = 'Take Out'
        elif delivery_method == 'Delivery':
            new_status = 'Out for Delivery'

    if current_index == 2 and delivery_method == 'Delivery':
        if current_status == 'Cooking':
            new_status = 'Out for Delivery'

    if current_index == 3 and delivery_method == 'Take Out':
        if current_status == 'Take Out':
            new_status = 'Done'

    orders.update_one({'_id': ObjectId(order_id)}, {
                      '$set': {'Status': new_status}})


@app.route('/dashboard')
def dashboard():
    orders = get_order_data()
    # Format date and time in the orders
    for order in orders:
        # Assuming 'Date' is the field containing the date and time
        if 'Date' in order:
            # Assuming the date is stored as a string or a datetime object
            date_obj = order['Date']
            if isinstance(date_obj, str):
                # Convert the string to a datetime object
                # Adjust the format if needed
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
            # Format date and time as desired
            order['Date'] = date_obj.strftime('%d %B %Y, %H:%M')
    return render_template('dashboard.html', orders=orders)


@app.route('/update_status', methods=['POST'])
def update_order_status():
    order_id = request.form['order_id']
    update_status(order_id, request.form['new_status'])
    return redirect('/dashboard')


@app.route('/delete_order', methods=['POST'])
def delete_order():
    order_id = request.form['order_id']
    orders.delete_one({'_id': ObjectId(order_id)})
    return redirect('/dashboard')


## CART CODE ##
def start_session():
    session['uid'] = uuid.uuid4()
    log_data = {
        'timestamp': datetime.now(),
        'session_id': session['uid'],
        'path': request.path,
        'method': request.method,
        'ip_address': request.remote_addr
    }
    sessions.insert_one(log_data)
    return log_data


def add_order(name, phone, address, postcode, delivery_method, order, status='Not Started'):
    # Get the current date and time
    current_date = datetime.now()

    # Prepare order data
    order_data = {
        'Date': current_date,
        'Name': name,
        'Phone': phone,
        'Address': address,
        'Postcode': postcode,
        'DeliveryMethod': delivery_method,
        'Order': order,
        'Status': status
    }

    orders.insert_one(order_data)


## Home Page ##

@app.route('/')
def home():
    return render_template('index.html')


## Tracker ##

@app.route('/tracker-login', methods=['GET', 'POST'])
def tracker_login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        order = orders.find_one({'Phone': phone_number})
        if order:
            return redirect(url_for('tracker', phone_number=phone_number))
        else:
            return "Phone number not found. Please try again."

    return render_template('tracker_login.html')


@app.route('/tracker/<phone_number>')
def tracker(phone_number):
    order = orders.find_one({'Phone': phone_number})
    if order:
        return render_template('tracker.html', order=order, status=order['Status'])
    else:
        return "Order not found."


if __name__ == '__main__':
    app.run(debug=True)
