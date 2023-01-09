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

@bp.route('/categories/<category>')
def get_records_in_category(category):
    db = get_db()
    records = db.execute(
        'SELECT b.id, b.user_id, b.username, b.name, b.cost, cu.name as cu_name, b.date '
        ' FROM ( SELECT a.id, a.user_id, a.username, c.name, a.cost, a.currency_id, a.date' 
        ' from ( SELECT r.id, r.user_id, u.username, r.category_id, r.cost, r.currency_id, r.date '
        ' FROM records r JOIN users u ON r.user_id = u.id) as a JOIN categories c ON a.category_id = c.id) as b '
        ' JOIN currencies cu ON b.currency_id=cu.id'
        ' WHERE b.user_id=? and b.name = ?',
        ( g.user['id'],category, ) 
    ).fetchall()

    if len(records) == 0:
        abort(404, f"You have no no records in this category ...")

    return render_template('records/index.html', records=records)

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