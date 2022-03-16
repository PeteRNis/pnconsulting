################################################################################
#######################    Setting up views for posts    #######################
################################################################################

# imports
from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from project_1 import db
from project_1.models import BlogPost
from project_1.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts',__name__)

# We want views for (CRUD)
#   1. CREATE a blogpost
#   2. Viewing a blogpost
#   3. Updating a blogpost
#   4. Deleting a blogpost

# create
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                                text=form.text.data,
                                user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)

# view
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
                            date=blog_post.date, post=blog_post)

# update
# Here we check if the user visiting is actually the author,
# if not, they are not able to update.
# Then we reset the title and text to the title and text in the update form
# and eventually we commit those changes to the db
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', title='Updating', form=form)

# delete
@blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
