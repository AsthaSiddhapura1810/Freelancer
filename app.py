from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import stripe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freelancer.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Configure Stripe
stripe.api_key = 'your_stripe_secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    account_id = db.Column(db.String(120), nullable=True)  # Stripe Account ID

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        budget = request.form['budget']
        project = Project(title=title, description=description, budget=budget, client_id=1)  # Example client
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_project.html')

@app.route('/connect_stripe')
def connect_stripe():
    account = stripe.Account.create(type='express')
    user = User.query.get(1)  # Example user
    user.account_id = account.id
    db.session.commit()
    return f"Connected with Stripe Account: {account.id}"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
