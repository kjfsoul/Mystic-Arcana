from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from replit import db
from datetime import datetime
from utils.openai_client import generate_blog_post

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

# Sample blog posts for initial display
SAMPLE_POSTS = [
    {
        'id': '1',
        'title': 'Understanding Tarot Cards',
        'content': 'Tarot cards are a powerful tool for divination and self-discovery...',
        'date': '2023-05-15',
        'author': 'Mystic Guide',
        'category': 'Tarot',
        'image': '/static/images/tarot-blog.jpg'
    },
    {
        'id': '2',
        'title': 'Mercury Retrograde: What It Means For You',
        'content': 'When Mercury goes retrograde, communication and technology may be affected...',
        'date': '2023-05-10',
        'author': 'Astrology Expert',
        'category': 'Astrology',
        'image': '/static/images/mercury-retrograde.jpg'
    }
]

@blog_bp.route('/')
def blog_home():
    # Get posts from database
    if 'blog_posts' not in db:
        db['blog_posts'] = SAMPLE_POSTS

    posts = db['blog_posts']
    return render_template('blog.html', posts=posts)

@blog_bp.route('/post/<post_id>')
def blog_post(post_id):
    # Find the post with the given ID
    posts = db.get('blog_posts', SAMPLE_POSTS)
    post = next((p for p in posts if p['id'] == post_id), None)

    if not post:
        return redirect(url_for('blog.blog_home'))

    return render_template('blog_post.html', post=post)

@blog_bp.route('/category/<category>')
def blog_category(category):
    posts = db.get('blog_posts', SAMPLE_POSTS)
    category_posts = [p for p in posts if p['category'].lower() == category.lower()]

    return render_template('blog_category.html', 
                          category=category,
                          posts=category_posts)

# Admin-only routes (would need proper authentication in production)
@blog_bp.route('/admin/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')

        if not title or not content or not category:
            flash('Please fill in all required fields')
            return render_template('new_post.html')

        # Create a new post
        new_post = {
            'id': str(datetime.now().timestamp()),
            'title': title,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': session.get('username', 'Admin'),
            'category': category,
            'image': request.form.get('image', '/static/images/default-blog.jpg')
        }

        # Add to database
        if 'blog_posts' not in db:
            db['blog_posts'] = SAMPLE_POSTS

        posts = db['blog_posts']
        posts.append(new_post)
        db['blog_posts'] = posts

        flash('Blog post created successfully!')
        return redirect(url_for('blog.blog_home'))

    return render_template('new_post.html')