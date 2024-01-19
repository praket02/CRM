# Import necessary modules and libraries
import arrow
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# connecting to the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crm_db.sqlite3"

# Initialize the SQLAlchemy database extension
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

#-----------------------------------------------------------

# Defining the Complaint model for the database
class Complaint(db.Model):
    __tablename__ = "complaints_data"

    complaint_id = db.Column(db.String, nullable=False, unique=True, primary_key=True, autoincrement=False)
    customer_name = db.Column(db.String, nullable=False, unique=False, primary_key=False, autoincrement=False)
    phone_number = db.Column(db.String, nullable=False, unique=False, primary_key=False, autoincrement=False)
    address = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    # Defining a method to convert Complaint object to dictionary
    def todict(self):
        return {
            'complaint_id': self.complaint_id,
            'customer_name': self.customer_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'status': self.status
        }

    # Defining a method to get values of the Complaint object
    def values(self):
        return [self.complaint_id, self.customer_name, self.phone_number, self.address, self.status ]

#------------------------------------------

# Defining a function to generate the next complaint ID based on the current date
def next_cid(prev):
    prev = prev.split("-")[1:]
    now = arrow.now().format('YYYYMMDD')

    if prev[0] == now:
        seq = str(int(prev[1])+1)
        if len(seq)<4:
            seq = '0'*(3-len(seq)) + seq

        return f"CRM-{now}-{seq}"
    else:
        return f"CRM-{now}-001"

# function to convert a list of Complaint objects to a list of dictionaries   
def complaints_list(l):
    return list(map(lambda complaint: complaint.todict(), l))

#---------------------------------------------

# Defining the root route, redirects to the 'dash' route
@app.route("/")
def root():
    return redirect(url_for('dash'))

# Define the 'dash' route.
@app.route("/dash/")
def dash():
    complaints = complaints_list(Complaint.query.all())
    return render_template("dash.html", complaints=complaints )

# Defining the route to create a new complaint
@app.route("/dash/new", methods=["GET", 'POST'])
def new_complaint():
    if request.method == 'GET':
        return render_template("new_complaint.html")
    elif request.method == 'POST':
        customer_name = request.form["customer_name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]
        status = 'OPEN'

        try:
            prev_cid = Complaint.query.all()[-1].complaint_id
            complaint_id = next_cid(prev_cid)
        except IndexError:
            complaint_id = f"CRM-{arrow.now().format('YYYYMMDD')}-001"

        complaint = Complaint(
            complaint_id = complaint_id,
            customer_name = customer_name,
            phone_number = phone_number,
            address = address,
            status = status 
        )

        db.session.add(complaint)
        db.session.commit()       

        return redirect(url_for('dash'))

# Defining the route to close a complaint
@app.route("/dash/close", methods=['POST'])
def closing():
    complaint_key = request.data.decode('utf-8')
    complaint = Complaint.query.filter_by(complaint_id=complaint_key).first()
    
    if complaint:
        complaint.status = 'CLOSED'
        db.session.commit()

    return url_for('dash')

# Defining the route to modify a complaint
@app.route("/dash/modify/<complaint_id>", methods=['GET', 'POST'])
def modify_complaint(complaint_id):
    complaint = Complaint.query.filter_by(complaint_id=complaint_id).first()

    if request.method == 'GET':
        return render_template('modify_complaint.html', complaint=complaint)
    if request.method == 'POST':
        customer_name = request.form["customer_name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]
        status = request.form['status']

        if complaint:
            complaint.customer_name = customer_name
            complaint.phone_number = phone_number
            complaint.address = address
            complaint.status = status 

            db.session.add(complaint)
            db.session.commit()

        return redirect(url_for('dash'))


#----------------------------------------------

# Running the Flask application if the script is executed directly
if __name__ == "__main__":
    app.run(
        debug = False,
        host = "127.0.0.1",
        port = 5000
    )


