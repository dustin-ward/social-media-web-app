from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from password import *
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        createUsername = request.form['username']
        createEmail = request.form['email']
        createPassword = request.form['password']

        saltPassword = salt_password(createPassword)
        hashPassword = bcrypt.generate_password_hash(saltPassword)

        try:
            newUser = User(username = createUsername, email = createEmail, password = hashPassword)
            db.session.add(newUser)
            db.session.commit()
        except:
            print("Error creating account")
            return redirect('/')
        return redirect('/')

    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginUsername = request.form['username']
        loginPassword = request.form['password']

        saltPassword = salt_password(loginPassword)

        return redirect('/')

    return render_template('auth/login.html')

if __name__ == '__main__':
    app.run(debug=True)
