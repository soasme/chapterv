# -*- coding: utf-8 -*-

from flask import url_for, redirect, render_template
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from app.utils.forms import save_form_obj
from app.utils.view import templated, ensure_resource
from app.utils.transaction import transaction
from app.models import Topic, TopicFollow
from app.forms import TopicForm
from app.core import db
from .core import bp

@bp.route('/topics', defaults={'page': 1})
@templated('web/topic/list.html')
def get_topics(page):
    return dict(
        pagination=Topic.query.filter_by(user_id=current_user.id).paginate(page),
    )

@bp.route('/topics/add', methods=['GET', 'POST'])
@transaction(db)
@login_required
@templated('web/topic/add.html')
def add_topic():
    topic = Topic(user_id=current_user.id)
    return save_form_obj(
        db, TopicForm, topic,
        build_next=lambda form, topic: url_for('web.get_topic_issues', id=topic.id),
    )

@bp.route('/topics/<int:id>/update', methods=['GET', 'POST'])
@transaction(db)
@login_required
@templated('web/topic/update.html')
@ensure_resource(Topic)
def update_topic(id, topic):
    return save_form_obj(
        db,
        TopicForm,
        obj=topic,
        build_next=lambda form, topic: url_for('web.get_topic_issues', id=id),
        before_render_map=['obj->topic'],
    )

@bp.route('/topics/<int:id>/follow')
@login_required
def follow_topic(id):
    try:
        topic = Topic.query.get_or_404(id)
        follow = TopicFollow(user_id=current_user.id, topic_id=topic.id)
        db.session.add(follow)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return redirect(url_for('web.get_topic', id=topic.id))
