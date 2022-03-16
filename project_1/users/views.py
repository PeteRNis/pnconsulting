################################################################################
# We need to create the views for:
#   1. Register a user
#   2. Login a user
#   3. Logout a user
#   4. Show an account
#   5. Users list of posts (væg)
#
# Therefore, we have to make a few imports in regard to templates, redirections
# blueprints, user functionality, database interaction, models, forms and picture
################################################################################
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project_1 import db
from project_1.models import User, BlogPost
from project_1.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from project_1.users.picture_handler import add_profile_pic

# First we will register this as a blueprint
users = Blueprint('users',__name__)

################################################################################
#   1. Registration view
# We link it to registrationform, and say, if it validates on submit we create
# a user object based on the elements we acquire at form.column.data
# in the db.session we add and commit it to our database, and redirects the user
# to the login page. But if we do not return render template at the end,
# we wont have a view for the registration page itself
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Your user has been created')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


################################################################################
#   2. Login view
# As opposed to the registration view, we do not want to create, we just want to
# query, and check if the user already has a spot in our database
# Upon logging in, they provide an email address, and we are filtering by that mail.
# Often a usear are searching for something is prompted to login,
# there we have our next object to
@users.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.validate_password(form.password.data) and user is not None:

            login_user(user)
            flash('You are now logged in')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)

    return render_template('login.html',form=form)


################################################################################
#   3. Logout view
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


################################################################################
#   4. Account
# First, you need to be logged in, to edit the profile
# If people actually submittet something to the picture filefield in forms,
# then the if form.picture.data: gets activated. The if statement, grabs the UserName
# and pass that in to the add_profile_pic function we defined in picture_handler.py.
# Then we take the attribute profile_image, specified in models.py and say its now equal to pic
@users.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated')
        return redirect(url_for('users.account'))

    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

################################################################################
#   5. Wall / user post view
# When you go to your website/username, we will pass the username,
# grab the page, using the page variable, that will allow us to cycle through pages.
# Then we will query for that user. Here we use the method .first_or_404 to ensure
# that they will get redirected to our 404 if they type it out wrong.
# Once we have the user, we will grab the blog post, created in models and say
# author = user (our foreign key relationship specified in models).
# Then we will order it by blogpost date in decending order.
# Then we call the paginate function to ensure that we get actual pages
# eventually we return the html page using render_template
@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
