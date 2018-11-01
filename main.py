from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql, requests
from forms import UserLogin, UserSignup, Add_Blog
from wtforms_sqlalchemy.fields import QuerySelectField
from bs4 import BeautifulSoup
#=============================================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "a7d473df2aa95f2e786acae2b1024afd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:hwdi9100@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#================================================================================
#Create Your Classes (Each class is a table and each variable is a column)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    username = db.Column(db.String(25), nullable=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), default="No password input")
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    blogs = db.relationship("Blog", backref="author", lazy=True)


def __repr__(self):
    return f'User("{self.username}", "{self.password}", "{self.email}", "{self.image_file}")'


#===============================================================================

class Blog (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))


def __repr__(self):
    return f'Blog("{self.heading}", "{self.body}", "{self.date_posted}", "{self.user_id}")'




#============================================================================


#Create Your routes

@app.route("/")
def index():

    return render_template("index.html", title="Welcome")

#===========================================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserSignup()
    if form.validate_on_submit():
        # If all input is valid when you hit submit will go to "welcome.html"
        return render_template("login.html", form=form, title="Welcome")
    # If any of input is not valid when you hit submit will go back to "signup.html"
    return render_template("signup.html", form=form, title="Signup")

#===========================================================================
#===========================================================================



#===========================================================================
#===========================================================================


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()
    errors = None
    
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username = username).first()
        
        if user and user.password == password:
            return redirect("/newpost")
           
    # If any of input is not valid when you hit submit will go back to "signup.html
        else: 
            error = "Invalid Credntials. Please try again."
    return render_template("login.html", form=form, title="Login", errors = errors)

    

#===========================================================================

@app.route("/blog")
def display_blogs():
    form = Add_Blog()
    blogs = Blog.query.all()
    
    return render_template("blog.html", form=form, title="All Post", blogs=blogs)
 
#===========================================================================


@app.route("/newpost",  methods=["POST", "GET"])
def add_new_post():
    form = Add_Blog()
    
    if request.method == "POST":
        input_title = form.heading.data
        input_body = form.body.data
        blog_id = request.form["blog-id"]
        new_blog = Blog(heading=input_title, body=input_body)
        db.session.add(new_blog)
        db.session.commit()
        
        blogs = Blog.query.all()
      

    if form.validate_on_submit():
        # If all input is valid when you hit submit will go to "welcome.html"
        return render_template("blog.html", form=form, title="Added Post", blogs=blogs)
    # If any of input is not valid when you hit submit will go back to "signup.html"
    return render_template("newpost.html", title="Add new Post!", form=form)

#===========================================================================


@app.route("/added_post", methods=["POST", "GET"])
def added_post():
    form = Add_Blog()
    
    blog_id = request.args.get("blog-id")
    blog = Blog.query.get(blog_id)
    
    
    return render_template("added_post.html", title="Added Post!", form=form , blog= blog)
#===========================================================================


@app.route("/logout")
def logout():
    form = UserLogin()
    return render_template("logout.html", form=form, title="Logged Out")

#============================================================================
if __name__ == '__main__':
    app.run(debug=True)
