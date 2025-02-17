from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b330ca4b39c340463510ebd2fb7304f0'
app.congig["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

books = [
    {
        "author": "J.K. Rowling",
        "title": "Harry Potter and the Sorcerer's Stone",
        "content": "The story follows young Harry Potter as he discovers his magical heritage and attends Hogwarts School of Witchcraft and Wizardry, where he makes friends and faces dark challenges."
    },
    {
        "author": "George Orwell",
        "title": "1984",
        "content": "A dystopian novel set in a totalitarian society under constant surveillance. The protagonist, Winston Smith, struggles to maintain his individuality and sanity."
    },
    {
        "author": "Jane Austen",
        "title": "Pride and Prejudice",
        "content": "The novel explores the complex nature of love, reputation, and class distinctions through the romantic entanglements of Elizabeth Bennet and Mr. Darcy."
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', books=books, title="Books")

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods = ["POST","GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created for {form.username.data}!","success")
        return redirect(url_for('home'))
    return render_template('register.html',title="Register",form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html',title="Login",form=form)


if __name__ == "__main__":
    app.run(debug=True)