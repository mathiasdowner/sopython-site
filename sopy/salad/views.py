from flask import jsonify
from flask_wtf import Form
from sopy import db
from sopy.ext.views import template, redirect_for
from sopy.salad import bp
from sopy.salad.forms import SaladForm
from sopy.salad.models import Salad


@bp.route('/')
@template('salad/index.html')
def index():
    items = Salad.query.order_by(Salad.position).all()

    return {'items': items}


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@template('salad/update.html')
def update(id=None):
    item = Salad.query.get_or_404(id) if id is not None else None
    form = SaladForm(obj=item)

    if form.validate_on_submit():
        if item is None:
            item = Salad()
            db.session.add(item)

        form.populate_obj(item)
        db.session.commit()

        return redirect_for('salad.index')

    return {'item': item, 'form': form}


@bp.route('/<int:id>/move_up', endpoint='move_up')
@bp.route('/<int:id>/move_down', endpoint='move_down', defaults={'down': True})
def move(id, down=False):
    item = Salad.query.get_or_404(id)

    if down:
        item.move_down()
    else:
        item.move_up()

    db.session.commit()

    return redirect_for('salad.index')


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@template('salad/delete.html')
def delete(id):
    item = Salad.query.get_or_404(id)
    form = Form()

    if form.validate_on_submit():
        item.delete()
        db.session.commit()

        return redirect_for('salad.index')

    return {'item': item, 'form': form}
