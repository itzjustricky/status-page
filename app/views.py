"""
    Views for the test page

"""

import sys
import os.path

import pandas as pd
import sklearn.datasets as datasets

from app import app

import flask
from flask import render_template
# from flask import redirect

# import custom modules in directory of app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pagination import Paginator

PER_PAGE = 20
boston_data = datasets.load_boston()
boston_data_df = pd.DataFrame(boston_data.data, columns=boston_data.feature_names)


@app.route('/index/', defaults={'page': 1})
@app.route('/index/page/<int:page>')
def show_users(page):
    # count = count_all_users()
    # users = get_users_for_page(page, PER_PAGE, count)
    count = boston_data_df.shape[0]

    pagination = Paginator(page, PER_PAGE, count)
    if page < 1 or page > pagination.n_pages:
        flask.abort(404)

    start_ind = (page - 1) * PER_PAGE
    end_ind = page * PER_PAGE
    return render_template(
        'index.html',
        html_table=boston_data_df.loc[start_ind:end_ind].to_html(
            index=False, border=0, classes='table table-condensed table-hover'),
        pagination=pagination,
    )


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
