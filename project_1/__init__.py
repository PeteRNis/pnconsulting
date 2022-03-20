################################################################################
# This file holds lot of our organizational logic connecting the database, the #
# migrate function blueprints, the login manager etc. The page similarely
# cointain the various imports we do throughout the project.
#
################################################################################
import os
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask(__name__)

# adding CKEditor
ckeditor = CKEditor(app)

# While we begin setting up our models, we can take advantage of developing on #
# the database right away. In that way, we would make less mistakes.           #

################################################################################
######################  Setting up the configurations   ########################
################################################################################
app.config['SECRET_KEY'] = 'mysecret'


################################################################################
############################   Database setup   ################################
################################################################################

# to get the basedir, we have to import our operating system, os.
basedir =os.path.abspath(os.path.dirname(__file__))

# SQLLite db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')

# New mysql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Kode0487@localhost/newusers'

# Postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://demvwzifmoqccj:018ed330e525c224f2fd374b66263dee314d58b2dfe4ed2f23a0a396f6813645@ec2-3-216-221-31.compute-1.amazonaws.com:5432/d1h6mmt5sjp61m'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


################################################################################
######################      Login configurations    ############################
################################################################################

# This is imported, because we need the methods inside our models.py
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

################################################################################
################    Blueprint registrations for all views     ##################
################################################################################

# here we import the blueprint from core.views.py
from project_1.core.views import core
app.register_blueprint(core)

# here we import the error page handlers
from project_1.error_pages.handlers import error_pages
app.register_blueprint(error_pages)

# here we import the blueprint created in users.views.py
from project_1.users.views import users
app.register_blueprint(users)

from project_1.blog_posts.views import blog_posts
app.register_blueprint(blog_posts)
