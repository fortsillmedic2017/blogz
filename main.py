from flask import Flask, request, redirect, url_for, render_template, flash,session
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
#================================================================================


class Blog (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))


def __repr__(self):
    return f'Blog("{self.heading}", "{self.body}", "{self.date_posted}", "{self.owner}")'


#===============================================================================




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    username = db.Column(db.String(25), nullable=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), default="No password input")
    image_file = db.Column(db.String(20), nullable=False,default="default.jpg")
    blogs = db.relationship("Blog", backref="owner")


def __repr__(self):
    return f'User("{self.username}", "{self.password}", "{self.email}", "{self.image_file}")'

#============================================================================
#                        Create Your routes                                #
#============================================================================

#@app.before_request is not a regular@app.route, it is a function for session
#will run for every request to check if user is logged in
# tells Flask to run this function before calling the rquest handler for the incomming request

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

# the "username" not in session check to see if ("username", "email", ect..) is in a session if
#not then you wil be forced to log in if want to enter site

#above is checking to see if request.endpoint(the destination of the request)
#not in the allowed_routes dictionary above  and also checking too see
#if session["x"] to see if "x " is in the session dictionary (session["username"])
# so checking to see if both are True, if so then will reidrect to "/login"
# If False will skip over the abouve route and continue to login



#===========================================================================

@app.route("/")
def index():

    return render_template("index.html", title="Home")

#===========================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()
    errors = "User password is incorrect or User does not exsis."
    #Check data database by what was entered into the signup form
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

#We want to now take the infor that was added by the above and query it to check if user exsist
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            
#session['x'] is dic. = real value(userename, email, password ect...)
           session['username'] = username #the @app.before_request above will check
           flash("Logged in")
           print(session)
           return redirect("/newpost")
           
    # If any of input is not valid when you hit submit will display message below:
    #TODO - need better response message
        else: 
            #flash("User password is incorrect or User does not exsist")
            return render_template("login.html", form=form, title="Login", errors=errors)
           
    return render_template("login.html", form=form, title="Login")


#===========================================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserSignup()
    errors = "Duplicate Data Entered. Data already in Database"
    
    if request.method == "POST" and form.validate_on_submit(): #validation
    #Add data to database by what was entered into the signup form fields
        username = form.username.data
        email = form.email.data
        password = form.password.data

#We want to now take the infor that was added by the above and query it to check credetials
#can use filter_by().first() if have one column that is unique
        
#ChecK if user already exsist:
        existing_user = User.query.filter_by(username = username).first()
#If don't exsist will  create that user 
        if not existing_user:
            new_user = User(username=username, email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
#If user exsist will:
            return redirect("/login")
        else:
            #TODO - better response message if user exsist
          # errors = "Duplicate Data Enter. Data already in Database"
           return render_template("signup.html", form=form, title="Signup", errors=errors)
    return render_template("signup.html", form=form, title="Signup")


#===========================================================================

@app.route("/blog", methods=["POST", "GET"])
def display_blogs():
    form = Add_Blog()
    blogs = Blog.query.all()
    users = User.query.all()
    
    return render_template("blog.html", form=form, title="All Post", blogs=blogs,
    users = users)
 
#===========================================================================


@app.route("/newpost",  methods=["POST", "GET"])
def add_new_post():
    form = Add_Blog()

    owner = User.query.filter_by(username=session["username"]).first()
#This get the username of current loggin user out od the session
#then it filter the result by username and get the first one
#should only be one bc username is unque
#this would put the result in the owner variable
#then you can create a new_blog with that owner
 #This is how you get the owner of blog(as long as they are logged in b/c of session ["username"] above)

    
    if request.method == "POST":
        input_title = form.heading.data
        input_body = form.body.data

        #blog_id = request.form["blog-id"]
        new_blog = Blog(heading=input_title, body=input_body, owner = owner  )
        db.session.add(new_blog)
        db.session.commit()
        
        blogs = Blog.query.filter_by(owner = owner).all()
      

    if form.validate_on_submit():
        # If all input is valid when you hit submit will go to "welcome.html"
        return render_template("blog.html", form=form, title="Added Post", blogs=blogs)
    # If any of input is not valid when you hit submit will go back to "signup.html"
    return render_template("newpost.html", title="Add new Post!", form=form)

#===========================================================================



@app.route("/singleUser")
def user_html():
    form = Add_Blog()
    
    blog_id = request.args.get("blog-id")
    blog = Blog.query.get(blog_id)

    
    
    return render_template("added_post.html", title="Added Post!", form=form , blog= blog)
#===========================================================================


'''@app.route("/added_post", methods=["POST", "GET"])
def added_post():
    form = Add_Blog()
    blog_id = request.args.get("blog-id")
    blog = Blog.query.get(blog_id)
    
    return render_template("added_post.html", title="Users  Post!", form=form, blog= blog)'''

#===========================================================================





#===========================================================================



@app.route("/logout", methods=["GET"])
def logout():
    form = UserSignup()
    blogs = Blog.query.all()
#this del session["username"] will let you knoe if user ins login or not
    del session['username']
    return render_template("/blog.html", form=form, title="All Post", blogs=blogs)

#============================================================================
if __name__ == '__main__':
    app.run(debug=True)
