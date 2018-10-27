from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from forms import UserLogin, UserSignup, Add_Blog

#=============================================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "a7d473df2aa95f2e786acae2b1024afd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hwdi9100@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#================================================================================
#Create Your Classes (Each class is a table and each variable is a column)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    username = db.Column(db.String(25), nullable=True, unique=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    password = db.Column(db.String(60), nullable=False, default="No password input")
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    #posts = db.relationship("Blog", backref="author", lazy=True)


def __repr__(self):
    return f'User("{self.username}", "{self.email}", "{self.image_file}")'


#===============================================================================

class Blog (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(5000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


def __repr__(self):
    return f'Blog("{self.heading}", "{self.body}", "{self.date_posted}")'



#============================================================================


#Create Your routes

@app.route("/blog")
@app.route("/newpost", methods= ["POST", "GET"])
def add_new_post():
    form = Add_Blog()
    if request.method == "POST":
        new_title = Blog(heading = form.heading.data)
        new_body = Blog(body = form.body.data)
        db.session.add(new_title)
        db.session.add(new_body)
        db.session.commit()

    blogs = Blog.query.all()
    #headings = blogs.heading.all()
    #bodies= blogs.body.all()
    if form.validate_on_submit():
        # If all input is valid when you hit submit will go to "welcome.html"
        return render_template("blog.html", form=form, title="Posted Blogs", blogs=blogs)
    # If any of input is not valid when you hit submit will go back to "signup.html"
    return render_template("newpost.html", title="Add new Post!", form=form)



  

    
@app.route("/add_post")
def add_post():
    form = Add_Blog()
    #return render_template("newpost.html", title_m="Add A Post!")
    return render_template("add_post.html", title="Added This Post!", form = form)

#===========================================================================


@app.route("/")
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserSignup()

    if form.validate_on_submit():
        # If all input is valid when you hit submit will go to "welcome.html"
        return render_template("login.html", form=form, title="Welcome")
    # If any of input is not valid when you hit submit will go back to "signup.html"
    return render_template("signup.html", form=form, title="Signup")


@app.route("/login",  methods=["GET", "POST"])
def login():
    form = UserLogin()
    if form.validate_on_submit():
        # If all input is valid when you hit submit will go to "welcome.html"
        return render_template("blog.html", form=form, title="Blogs HomePage")
    # If any of input is not valid when you hit submit will go back to "signup.html
    return render_template("login.html", form=form, title="Login")


@app.route("/home")
def home():
    form = UserLogin()
    return render_template("home.html", title="Home Page", form=form)


@app.route("/welcome")
def welcome():
    form = UserSignup()
    return render_template("signup.html", title="Signup Page", form=form)







#============================================================================
if __name__ == '__main__':
    app.run(debug=True)
