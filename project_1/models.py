
################################################################################
# In this file we are going to set up our classes. We need to let the BlogPost #
# class be an inherited part of the User class. In order to do so, we will     #
# have to import libraries and modules. That should be done in __init__.py     #
#   - We also set up the hash functions here, to ensure the form of storage    #
#   - We will also import usermixin, which allow us to have functions such as, #
#     is authenticated, is active etc on our actual models, inside of templates#
#   - We will have to import datetime, as we use it in the blogpost class      #
#   -
################################################################################
from project_1 import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


# Here we import the login manager that is configured in our __init__.py file      #
# These allow us to do the if user is authenticated sort of stuff in our templates #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='3.PNG')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    about_author = db.Column(db.Text(120), nullable = True)
    password_hash = db.Column(db.String(128))


# then we would like to link a blogpost class to the user class                #
# backref, is what we use to define the relationship beween user and blogpost  #
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

# Here we are checking the user login password versus the password hash we have #
# stored in our database                                                        #
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

# Now we create some king of representation we can print out to the user        #
    def __repr__(self):
        return f"Username: {self.username}"

class BlogPost(db.Model):

    users = db.relationship(User)
# users.id means the attribute id from the users class
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image = db.Column(db.String(36))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self,title,text,user_id, image=None):
        self.title = title
        self.text = text
        self.user_id = user_id
        self.image = image

# Finally we create a way to print out the text from the blogpost. Hopefully   #
# it shouldnt print, otherwise we will have to do some debugging               #
    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"
