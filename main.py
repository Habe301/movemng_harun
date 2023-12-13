from flask import Flask, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key for security
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Datenbankmigration
with app.app_context():
    db.create_all()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(500), nullable=True)

# Login-System
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Login-Manager Konfiguration
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Beispielroute für Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))  # Ändere 'dashboard' zu deiner gewünschten Startseite
    return render_template('login.html', form=form)

# Beispielroute für geschützte Seite, die nur eingeloggte Benutzer sehen können
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Beispielroute für Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Beispielroute für Startseite
@app.route("/")
def startpage():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
