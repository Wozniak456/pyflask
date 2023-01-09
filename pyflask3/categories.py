from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from pyflask3.auth import login_required
from pyflask3.db import get_db

bp = Blueprint('categories', __name__)

@bp.route('/categories')
def index():
    db = get_db()
    categories = db.execute(
        'SELECT * FROM categories'
        ' ORDER BY name'
    ).fetchall()
    return render_template('categories/category.html', categories=categories)

@bp.route('/categories/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO categories (name)'
                ' VALUES (?)',
                (name,)
            )
            db.commit()
            return redirect(url_for('categories.index'))

    return render_template('categories/create.html')