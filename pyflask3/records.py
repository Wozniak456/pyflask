from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from pyflask3.auth import login_required
from pyflask3.db import get_db

bp = Blueprint('records', __name__)

@bp.route('/')
def index():
    db = get_db()
    records = db.execute(
        'SELECT b.id, b.user_id, b.username, b.name, b.cost, cu.name as cu_name, b.date FROM'
        ' (SELECT a.id, a.user_id, a.username, c.name, a.cost, a.currency_id, a.date from'
        ' (SELECT r.id, r.user_id, u.username, r.category_id, r.cost, r.currency_id, r.date FROM records r JOIN users u '
        ' ON r.user_id = u.id) as a JOIN categories c '
        ' ON a.category_id = c.id) as b JOIN currencies cu '
        ' ON b.currency_id=cu.id '
        ' ORDER BY date DESC '
    ).fetchall()
    return render_template('records/index.html', records=records)

@bp.route('/<user_id>')
def get_records_by_id(user_id):
    db = get_db()
    records = db.execute(
        'SELECT b.id, b.user_id, b.username, b.name, b.cost, cu.name as cu_name, b.date '
        ' FROM ( SELECT a.id, a.user_id, a.username, c.name, a.cost, a.currency_id, a.date' 
        ' from ( SELECT r.id, r.user_id, u.username, r.category_id, r.cost, r.currency_id, r.date '
        ' FROM records r JOIN users u ON r.user_id = u.id) as a JOIN categories c ON a.category_id = c.id) as b '
        ' JOIN currencies cu ON b.currency_id=cu.id'
        ' WHERE b.user_id=?',
        (user_id,)
    ).fetchall()

    if len(records) == 0:
        abort(404, f"User id {user_id} doesn't exist.")

    return render_template('records/index.html', records=records)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():

    categories = get_db().execute(
                'select id, name from categories group by name order by id'
            ).fetchall()

    currencies = get_db().execute(
                'select id, name from currencies group by name order by id'
            ).fetchall()

    if request.method == 'POST':
        category_id = request.form['category_id']
        currency_id = request.form['currency_id']
        cost = request.form['cost']

        error = None

        if not category_id:
            error = 'category_id is required.'

        if not currency_id:
            error = 'currency_id is required.'

        if not cost:
            error = 'Cost is required.'

        if error is not None:
            flash(error)
        else:
            get_db().execute(
                'INSERT INTO records (user_id, currency_id, category_id, cost)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], currency_id, category_id, cost,)
            )
            get_db().commit()
            return redirect(url_for('records.index'))

    return render_template('records/create.html', categories=categories, currencies=currencies)

def get_post(id, check_author=True):
    record = get_db().execute(
        # 'SELECT b.id, b.user_id, b.username, b.name, b.cost, cu.name, b.date FROM'
        # ' (SELECT a.id, a.user_id, a.username, c.name, a.cost, a.currency_id, a.date from'
        # ' (SELECT r.id, r.user_id, u.username, r.category_id, r.cost, r.currency_id, r.date FROM records r JOIN users u '
        # ' ON r.user_id = u.id) as a JOIN categories c '
        # ' ON a.category_id = c.id) as b JOIN currencies cu '
        # ' ON b.currency_id=cu.id '
        # ' WHERE b.id = ?',
        'select * from records where id = ?',
        (id,)
    ).fetchone()

    if record is None:
        abort(404, f"Record id {id} doesn't exist.")

    if check_author and record['user_id'] != g.user['id']:
        abort(403)

    return record

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    record = get_post(id)

    if request.method == 'POST':
        category_id = request.form['category_id']
        currency_id = request.form['currency_id']
        cost = request.form['cost']

        error = None
        db = get_db()

        categoryNum = db.execute(
            'SELECT * FROM categories where id = ?',
            (category_id,)
        ).fetchall()

        if len(categoryNum) == 0:
            error = 'no such category'
        
        currencyNum = db.execute(
            'SELECT * FROM currencies where id = ?',
            (currency_id,)
        ).fetchall()

        if len(currencyNum) == 0:
            error = 'no such currency'

        if not category_id:
            error = 'category_id is required.'
        if not currency_id:
            error = 'currency_id is required.'
        if not cost:
            error = 'Cost is required.'

        if error is not None :
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE records SET category_id = ?, currency_id = ?, cost = ? WHERE id = ?',
                (category_id, currency_id, cost, id,)
            )
            db.commit()
            return redirect(url_for('records.index'))

    return render_template('records/update.html', record=record)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM records WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('records.index'))