from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import ForumPost, ForumComment
from .decorators import doctor_only
from ..extensions import db

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/posts', methods=['POST'])
@jwt_required()
@doctor_only
def create_post():
    data = request.get_json()
    user = get_jwt_identity()
    post = ForumPost(title=data['title'], content=data['content'], author_id=user['id'])
    db.session.add(post)
    db.session.commit()
    return jsonify({"msg": "Post created", "post_id": post.id}), 201

@forum_bp.route('/posts', methods=['GET'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
@doctor_only
def add_comment(post_id):
    data = request.get_json()
    user = get_jwt_identity()
    comment = ForumComment(post_id=post_id, content=data['content'], author_id=user['id'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"msg": "Comment added", "comment_id": comment.id}), 201
