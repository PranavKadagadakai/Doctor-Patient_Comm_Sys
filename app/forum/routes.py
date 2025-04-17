from flask import Blueprint, request, jsonify, abort, render_template, redirect, url_for
from flask_login import current_user, login_required
from .models import ForumPost, ForumComment
from app.extensions import db
from .decorators import doctor_only

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/posts', methods=['POST'])
@login_required
@doctor_only
def create_post():
    data = request.form  # for HTML form posts (not JSON)
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400

    post = ForumPost(title=title, content=content, author_id=current_user.id)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('forum.forum_page'))

@forum_bp.route('/posts', methods=['GET'])
def list_posts():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return jsonify([{
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "author_id": p.author_id,
        "created_at": p.created_at.isoformat()
    } for p in posts])

@forum_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "created_at": post.created_at.isoformat(),
        "comments": [{
            "id": c.id,
            "content": c.content,
            "author_id": c.author_id,
            "created_at": c.created_at.isoformat()
        } for c in post.comments]
    })

@forum_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
@doctor_only
def add_comment(post_id):
    data = request.form
    content = data.get('content')

    if not content:
        return jsonify({"error": "Comment content required"}), 400

    comment = ForumComment(post_id=post_id, content=content, author_id=current_user.id)
    db.session.add(comment)
    db.session.commit()

    return jsonify({"msg": "Comment added", "comment_id": comment.id}), 201

@forum_bp.route('/forum', methods=['GET'])
@login_required
def forum_page():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('forum.html', posts=posts)
