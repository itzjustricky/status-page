"""
    Views for the test page

"""

import sys
import os.path

import pandas as pd
import sklearn.datasets as datasets

from app import app

import flask
from flask import url_for
from flask import request
from flask import render_template
# from flask import redirect

# import custom modules in directory of app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pagination import Paginator
from html_objects import HTMLPyObject

pd.set_option('display.max_colwidth', -1)

# Set an arbitrary dataframe
PER_PAGE = 20
boston_data = datasets.load_boston()
# boston_data_df = pd.DataFrame(boston_data.data, columns=boston_data.feature_names)
boston_data_df = pd.DataFrame(boston_data.data[:, :4], columns=boston_data.feature_names[:4])


def create_tickbox(tickbox_group, name, text=None):
    tickbox = HTMLPyObject('label', attrib={"class": "checkbox-inline"})
    input_obj = tickbox.sub_element(
        'input', attrib={
            "type": "checkbox",
            "name": tickbox_group,
            "value": name}
    )
    if text is not None:
        input_obj.text = text
    return tickbox


tickboxes = [create_tickbox('row_select', 'name_{}'.format(ind))
             for ind in range(boston_data_df.shape[0])]
boston_data_df.insert(0, ' ', tickboxes, allow_duplicates=True)


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def show_users(page):
    # count = count_all_users()
    # users = get_users_for_page(page, PER_PAGE, count)
    count = boston_data_df.shape[0]

    pagination = Paginator(page, PER_PAGE, count)
    # if page < 1 or page > pagination.n_pages:
    if page > pagination.n_pages and page > 1:
        flask.abort(404)

    start_ind = (page - 1) * PER_PAGE
    end_ind = page * PER_PAGE
    if boston_data_df.shape[0] == 0:
        html_table = boston_data_df.to_html(
            index=False, border=0, escape=False,
            classes='table table-condensed table-hover')
    else:
        html_table = boston_data_df[start_ind:end_ind].to_html(
            index=False, border=0, escape=False,
            classes='table table-condensed table-hover')

    return render_template(
        'index.html',
        html_table=html_table,
        pagination=pagination,
    )


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page
