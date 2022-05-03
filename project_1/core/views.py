from project_1.models import BlogPost
from flask import render_template, request, Blueprint, session
import numpy as np
import pandas as pd

core = Blueprint('core',__name__)

df = pd.DataFrame({'column 1 ': [4, 6, 1, 3, 7],
                   'column 2 ': [5, 6, 7, 8, 9],
                   'column 3 ': [5, 6, 7, 8, 9],
                   'column 4 ': [5, 6, 7, 8, 9],
                   'column 5 ': [5, 6, 7, 8, 9],
                   'column 6 ': [5, 6, 7, 8, 9],
                   'column 7 ': [5, 6, 7, 8, 9],
                   'column 8 ': [5, 6, 7, 8, 9],
                   'column 9 ': [5, 6, 7, 8, 9],
                   'column 10 ': [5, 6, 7, 8, 9],
                   'column 11 ': ['a', 'b', 'c', 'd', 'e']})

@core.route('/')
def index():
    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', blog_posts=blog_posts)

@core.route('/info')
def info():
    return render_template('info.html')

@core.route('/contact')
def contact():
    return render_template('contact.html')

@core.route('/cases')
def cases():
    return render_template('cases/cases.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
