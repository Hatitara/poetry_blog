from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from .models import *
from .forms import PoemForm
from . import db

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    poems = Poem.query.order_by(Poem.created_at.desc()).all()
    return render_template('index.html', poems=poems)

@home_bp.route('/submit', methods=['GET', 'POST'])
@login_required
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
            tags=form.tags.data,
            category=form.category.data,
            is_draft=form.is_draft.data,
            author=author_name,
            user_id=user_id
        )
        db.session.add(poem)
        db.session.commit()
        flash('Вірш збережено як чернетка' if poem.is_draft else 'Вірш опубліковано!', 'success')
        return redirect(url_for('home.index'))

    return render_template('submit.html', form=form)

@home_bp.route('/explore')
def explore():
    sort = request.args.get("sort", "new")

    query = Poem.query.filter_by(is_draft=False)

    if sort == "popular":
        poems = query.order_by(Poem.view_count.desc()).limit(30).all()
    else:
        poems = query.order_by(Poem.created_at.desc()).limit(30).all()

    return render_template("explore.html", poems=poems, sort=sort)


@home_bp.route('/feed')
@login_required
def feed():
    following_ids = [f.following_id for f in Follow.query.filter_by(follower_id=current_user.id).all()]

    poems = Poem.query.filter(
        Poem.user_id.in_(following_ids),
        Poem.is_draft == False
    ).order_by(Poem.created_at.desc()).limit(30).all()

    return render_template("feed.html", poems=poems)

@home_bp.route('/like/<int:poem_id>', methods=['POST'])
@login_required
def like(poem_id):
    existing = Like.query.filter_by(user_id=current_user.id, poem_id=poem_id).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(Like(user_id=current_user.id, poem_id=poem_id))
    db.session.commit()
    return redirect(request.referrer or url_for('home.index'))

@home_bp.route('/bookmark/<int:poem_id>', methods=['POST'])
@login_required
def bookmark(poem_id):
    existing = Bookmark.query.filter_by(user_id=current_user.id, poem_id=poem_id).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(Bookmark(user_id=current_user.id, poem_id=poem_id))
    db.session.commit()
    return redirect(request.referrer or url_for('home.index'))

@home_bp.route('/comment/<int:poem_id>', methods=['POST'])
@login_required
def comment(poem_id):
    content = request.form.get('content')
    if content:
        db.session.add(Comment(user_id=current_user.id, poem_id=poem_id, content=content))
        db.session.commit()
    return redirect(url_for('home.poem_detail', poem_id=poem_id))
