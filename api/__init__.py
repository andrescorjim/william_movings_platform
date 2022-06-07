"""
This API creates a server in GCP that allows the developer to connect
multiple platform applications in a portable manner.
"""

####
## Import libraries
####
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Flask instance
app = Flask(__name__)

####
## Database connections
####

# Local Database URI - Use if developing locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/wm'

# NOTE: format of GCP SQL connection string: 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<USER>:<PASSWORD>@/<DATABASE_NAME>?unix_socket=/cloudsql/<PUT-SQL-INSTANCE-CONNECTION-NAME-HERE>'

# GCP Database URI - Use if deployed to the cloud
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@/wmdatabase?unix_socket=/cloudsql/wm-project-351016:europe-west1:wm'

# Default SQLAlchemy configuration to not receive warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database instance
db = SQLAlchemy(app)

# Marshmallow instance
ma = Marshmallow(app)

####
## Creating database tables
####

# Customers table
class Customers(db.Model):
    """Defines Customer Table structure."""
    # Primary key
    customer_id = db.Column(db.String(100), primary_key=True)
    customer_name = db.Column(db.String(100))
    customer_email = db.Column(db.String(100))
    customer_phone_number = db.Column(db.String(250))
    #Relationships
    bookings = db.relationship('Bookings', backref ='customer')

    def __init__(self, customer_id, customer_name, customer_email, customer_phone_number):
        """Instantiating table structure, allowing the program to use it for specific queries."""
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone_number = customer_phone_number

# Employee table
class Employees(db.Model):
    """Defines employees Table structure."""
    # Primary key
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #Other rows
    employee_name = db.Column(db.String(100))
    employee_role = db.Column(db.String(100))
    employee_email = db.Column(db.String(100))
    employee_phone_number = db.Column(db.String(100))
    #Relationships
    booking_employee = db.relationship('Bookings', backref = 'bookings')

    def __init__(self, employee_id, employee_name, employee_role, employee_email, employee_phone_number):
        """Instantiating table structure, allowing the program to use it for specific queries."""
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.employee_role = employee_role
        self.employee_email = employee_email
        self.employee_phone_number = employee_phone_number

# Payments table
class Payments(db.Model):
    """Defines payments table"""
    # Primary key
    payment_id = db.Column(db.String(100), primary_key = True)
    # Others
    payment_amount = db.Column(db.Float)
    payment_outcome = db.Column(db.String(100))
    # Relationships
    booking_payment = db.relationship('Bookings', backref='payment')

    def __init__(self,payment_id,payment_amount,payment_outcome):
        """Instantiating table structure, allowing the program to use it for specific queries"""
        self.payment_id = payment_id
        self.payment_amount = payment_amount
        self.payment_outcome = payment_outcome

# Bookings table
class Bookings(db.Model):
    """Defined bookings table"""
    # Primary key
    booking_id = db.Column(db.String(100), primary_key = True)
    # Foreign keys
    payment_id = db.Column(db.String(100), db.ForeignKey('payments.payment_id'))
    customer_id = db.Column(db.String(100), db.ForeignKey('customers.customer_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_id"))
    # Other
    booking_date = db.Column(db.String(100))
    vehicle_type = db.Column(db.String(100))
    service_type = db.Column(db.String(100))
    service_date = db.Column(db.String(100))
    pick_up_location = db.Column(db.String(100))
    drop_off_location = db.Column(db.String(100))
    service_characteristics = db.Column(db.String(1000))
    service_cycles = db.Column(db.Integer)

    def __init__(self, booking_id, payment_id, customer_id, employee_id, booking_date, vehicle_type, service_type, 
                service_date, pick_up_location, drop_off_location, 
                service_characteristics, service_cycles):
        """Instantiating table structure, allowing the program to use it for specific queries"""
        self.booking_id = booking_id
        self.payment_id = payment_id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.booking_date = booking_date
        self.vehicle_type = vehicle_type
        self.service_type = service_type
        self.service_date = service_date
        self.pick_up_location = pick_up_location
        self.drop_off_location = drop_off_location
        self.service_characteristics = service_characteristics
        self.service_cycles = service_cycles

# Creating all tables
db.create_all()

# db.session.rollback()

####
## Create table schemas
####

class CustomersSchema(ma.Schema):
    """Schemas for serializing and deserializing customers data"""
    class Meta:
        fields = ('customer_id', 'customer_name', 'customer_email', 'customer_phone_number')
    
customer_schema = CustomersSchema()
customers_schema = CustomersSchema(many=True)

class EmployeesSchema(ma.Schema):
    """Schemas for serializing and desirializing employees data"""
    class Meta:
        fields = ('employee_id', 'employee_name', 'employee_role', 'employee_email', 'employee_phone_number')

employee_schema = EmployeesSchema()
employees_schema = EmployeesSchema(many = True)

class BookingsSchema(ma.Schema):
    """Schemas for serializing and desirializing bookings data"""
    class Meta:
        fields = ('booking_id', 'payment_id', 'customer_id', 'employee_id', 'booking_date', 'vehicle_type', 
                  'service_type', 'service_date', 'pick_up_location', 'drop_off_location', 'service_characteristics')

booking_schema = BookingsSchema()
bookings_schema = BookingsSchema(many = True)

class PaymentsSchema(ma.Schema):
    """Schemas for serializing and desirializing payments data"""
    class Meta:
        fields = ('payment_id', 'payment_amount', 'payment_outcome')

payment_schema = PaymentsSchema()
payment_schema = PaymentsSchema(many = True)

####
## API functions

####

# 'POST' method to create a new user
@app.route('/newuser', methods = ['POST'])
def create_user():
    """Using HTTP Method 'POST'.
        POST a JSON file containing product information
        to add new instance to the customers table"""
    customer_id = request.json['customer_id']
    customer_name = request.json['customer_name']
    customer_email = request.json['customer_email']
    customer_phone_number = request.json['customer_phone_number']

    new_user = Customers(customer_id, customer_name, customer_email, customer_phone_number)
    db.session.add(new_user)
    db.session.commit()

    return customer_schema.jsonify(new_user)

# 'POST' method to create a new booking
@app.route('/booking/new', methods = ['POST'])
def create_payment():
    """Using HTTP method POST to
    create a new booking instance in the database
    """
    # Create a new payment instance
    payment_id = request.json['payment_id']
    payment_amount = request.json['payment_amount']
    payment_outcome = request.json['payment_outcome']

    new_payment = Payments(payment_id, payment_amount, payment_outcome)
    db.session.add(new_payment)
    db.session.commit()

    # Create a new booking instance
    booking_id = request.json['booking_id']
    customer_id = request.json['customer_id']
    employee_id = request.json['employee_id']
    booking_date = request.json['booking_date']
    vehicle_type = request.json['vehicle_type']
    service_type = request.json['service_type']
    service_date = request.json['service_date']
    pick_up_location = request.json['pick_up_location']
    drop_off_location = request.json['drop_off_location']
    service_characteristics = request.json['service_characteristics']
    service_cycles = request.json['service_cycles']

    new_booking = Bookings(booking_id, payment_id, customer_id, employee_id, booking_date, vehicle_type, service_type, 
                service_date, pick_up_location, drop_off_location, 
                service_characteristics, service_cycles)
    
    db.session.add(new_booking)
    db.session.commit()

    return customer_schema.jsonify(new_payment)


# 'GET' method to view bookings specific to a customer
@app.route('/bookings/<bookingCustomerID>', methods=['GET'])
def get_customer_bookings(bookingCustomerID):
    """Using HTTP Method 'GET'.
    GET all bookings specific to a customer in a
    JSON format."""
    
    # Query to get all customer bookings
    customer_bookings = db.session.query(Bookings.booking_id, Payments.payment_id, Payments.payment_amount, 
                                        Payments.payment_outcome, Customers.customer_id, Employees.employee_id, 
                                        Employees.employee_name, Employees.employee_phone_number, Employees.employee_email,
                                        Bookings.booking_date, Bookings.vehicle_type, Bookings.service_type,
                                        Bookings.service_date, Bookings.pick_up_location, Bookings.drop_off_location,
                                        Bookings.service_characteristics, Bookings.service_cycles).select_from(
                                        Bookings).join(Payments).join(Customers).join(Employees).filter(
                                        Customers.customer_id == bookingCustomerID).all()

    ###
    # Passing data from the query onto a python dictionary, later converted into a json object, returned by the API
    ###
    user_bookings_list = []

    for booking in customer_bookings:
        user_bookings_list.append({
            "booking_id": booking[0],
            "payment_id": booking[1],
            "payment_amount": booking[2],
            "payment_outcome": booking[3],
            "customer_id": booking[4],
            "employee_id": booking[5],
            "employee_name": booking[6],
            "employee_phone_number": booking[7],
            "employee_email": booking[8],
            "booking_date": booking[9],
            "vehicle_type": booking[10],
            "service_type": booking[11],
            "service_date": booking[12],
            "pick_up_location": booking[13],
            "drop_off_location": booking[14],
            "service_characteristics": booking[15],
            "service_cycles": booking[16],
        })
    
    user_bookings_json = jsonify(user_bookings_list)

    return(user_bookings_json)


# 'GET' method to view all bookings
@app.route('/bookings', methods=['GET'])
def get_bookings():
    """Using HTTP Method GET to
    view all bookings ever created in the system"""
    
    all_bookings = db.session.query(Bookings.booking_id, Payments.payment_id, Payments.payment_amount, 
                                        Payments.payment_outcome, Customers.customer_id, Customers.customer_name, 
                                        Customers.customer_phone_number, Employees.employee_id, 
                                        Employees.employee_name, Employees.employee_phone_number, Employees.employee_email,
                                        Bookings.booking_date, Bookings.vehicle_type, Bookings.service_type,
                                        Bookings.service_date, Bookings.pick_up_location, Bookings.drop_off_location,
                                        Bookings.service_characteristics, Bookings.service_cycles).select_from(
                                        Bookings).join(Payments).join(Customers).join(Employees).all()
    
    ###
    # Passing data from the query onto a python dictionary, later converted into a json object, returned by the API
    ###
    all_bookings_list = []

    for booking in all_bookings:
        all_bookings_list.append({
            "booking_id": booking[0],
            "payment_id": booking[1],
            "payment_amount": booking[2],
            "payment_outcome": booking[3],
            "customer_id": booking[4],
            "customer_name": booking[5],
            "customer_phone_number": booking[6],
            "employee_id": booking[7],
            "employee_name": booking[8],
            "employee_phone_number": booking[9],
            "employee_email": booking[10],
            "booking_date": booking[11],
            "vehicle_type": booking[12],
            "service_type": booking[13],
            "service_date": booking[14],
            "pick_up_location": booking[15],
            "drop_off_location": booking[16],
            "service_characteristics": booking[17],
            "service_cycles": booking[18],
        })
    
    all_bookings_json = jsonify(all_bookings_list)

    return(all_bookings_json)

# 'DELETE' method to delete a booking
@app.route('/bookings/delete/<id>', methods=['DELETE'])
def delete_booking(id):
    """Using HTTP Method 'DELETE'.
        DELETE a booking instance from the database.
        A single booking is queried by passing a product
        ID through the URL"""
    booking = Bookings.query.get(id)
    db.session.delete(booking)
    db.session.commit()

    return booking_schema.jsonify(booking)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host='127.0.0.1', port=8080, debug=True)