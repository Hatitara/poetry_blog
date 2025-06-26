from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from .models import Poem
from .forms import PoemForm
from . import db

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    poems = Poem.query.order_by(Poem.created_at.desc()).all()
    return render_template('index.html', poems=poems)

@home_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    form = PoemForm()
    if form.validate_on_submit():
        is_anonymous = request.form.get('anonymous') == 'on'
        author_name = "Анонім"
        user_id = None

        if current_user.is_authenticated and not is_anonymous:
            author_name = current_user.username
            user_id = current_user.id

        poem = Poem(
            title=form.title.data,
            body=form.body.data,
            author=author_name,
            user_id=user_id
        )
        db.session.add(poem)
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template('submit.html', form=form)
