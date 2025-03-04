
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from replit import db
from datetime import datetime
from utils.openai_client import generate_blog_post

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

# Sample blog posts
SAMPLE_POSTS = [
    {
        "id": "1",
        "title": "The Seven-Planet Alignment of February 2025: A Cosmic Must-Know",
        "author": "Celeste Moonshadow",
        "date": "Feb 23, 2025",
        "category": "Astrology",
        "content": """
        <p>This rare alignment blends astronomical wonder with astrological power. Whether you're stargazing or seeking spiritual insights, this alignment is a moment to connect with the cosmos.</p>
        <p>On February 28, 2025, seven planets in our solar system will align in a rare celestial event that astronomers and astrologers alike are eagerly anticipating. This alignment will feature Mercury, Venus, Mars, Jupiter, Saturn, Uranus, and Neptune appearing in a relatively straight line as viewed from Earth.</p>
        <p>What makes this event particularly special is that all seven planets will be visible to the naked eye or with minimal equipment like binoculars, creating a spectacular viewing opportunity for enthusiasts and professionals around the world.</p>
        <h3>Astrological Significance</h3>
        <p>From an astrological perspective, this seven-planet alignment represents a powerful moment of cosmic harmony and potential transformation. The combined energies of these celestial bodies create a unique opportunity for spiritual growth, manifestation, and collective consciousness shifts.</p>
        """
    },
    {
        "id": "2",
        "title": "Integrating Tarot and Oracle Cards for Deeper Readings",
        "author": "Raven Nightshade",
        "date": "Feb 20, 2025",
        "category": "Tarot & Oracle",
        "content": """
        <p>While each deck has its own energy and purpose, combining them can create a powerful synergy that provides multi-layered guidance and insight for your spiritual journey.</p>
        <p>Tarot cards follow a structured system with Major and Minor Arcana, offering detailed insights into situations and energies. Oracle cards, on the other hand, are more fluid and often focus on specific themes or messages.</p>
        <h3>Complementary Approaches</h3>
        <p>When combined thoughtfully, tarot can provide the structural framework of a reading while oracle cards can add nuance, clarification, or spiritual guidance. This integration allows for a reading that addresses both practical concerns and spiritual dimensions.</p>
        """
    },
    {
        "id": "3",
        "title": "Ancient Moon Rituals for Modern Self-Care Practices",
        "author": "Luna Silvermist",
        "date": "Feb 18, 2025",
        "category": "Spiritual Wellness",
        "content": """
        <p>Discover how our ancestors harnessed lunar energy for healing and transformation, and how you can incorporate these timeless practices into your modern wellness routine.</p>
        <p>For thousands of years, cultures around the world have synchronized their spiritual practices with the phases of the moon. These ancient rituals weren't just superstition – they were practical ways to align human activities with natural cycles.</p>
        <h3>New Moon Intentions</h3>
        <p>The new moon represents beginnings and potential. Create a ritual where you write down intentions or goals you wish to manifest in the coming lunar cycle. Place these in a special container or altar space to revisit throughout the month.</p>
        <h3>Full Moon Release</h3>
        <p>The full moon is perfect for releasing what no longer serves you. Write down habits, thoughts, or situations you want to let go of, then safely burn the paper while visualizing these energies transforming into light.</p>
        """
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
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    # Check if user is an admin
    is_admin = False
    if 'users' in db and session['user_id'] in db['users']:
        is_admin = db['users'][session['user_id']].get('email') == 'admin@mysticarcana.com'
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        use_ai = request.form.get('use_ai') == 'on'
        
        if use_ai:
            # Generate post content with AI
            post_data = generate_blog_post(title, category)
            content = post_data['content']
        elif not content:
            flash('Content is required when not using AI', 'error')
            return render_template('new_post.html', is_admin=is_admin)
        
        if not title or not category:
            flash('Title and category are required', 'error')
            return render_template('new_post.html', is_admin=is_admin)
        
        new_post = {
            "id": str(datetime.now().timestamp()),
            "title": title,
            "author": db['users'][session['user_id']]['name'],
            "date": datetime.now().strftime("%b %d, %Y"),
            "category": category,
            "content": content,
            "ai_generated": use_ai
        }
        
        if 'blog_posts' not in db:
            db['blog_posts'] = SAMPLE_POSTS
        
        db['blog_posts'].append(new_post)
        
        return redirect(url_for('blog.blog_post', post_id=new_post['id']))
    
    return render_template('new_post.html', is_admin=is_admin)

@blog_bp.route('/admin/generate-batch', methods=['GET', 'POST'])
def generate_batch():
    """Generate a batch of AI blog posts"""
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    # Ensure the user is an admin
    if 'users' in db and session['user_id'] in db['users']:
        if db['users'][session['user_id']].get('email') != 'admin@mysticarcana.com':
            return redirect(url_for('blog.blog_home'))
    else:
        return redirect(url_for('profile.login'))
    
    if request.method == 'POST':
        # Generate 5 blog posts as requested
        blog_ideas = [
            {"title": "Top 5 Tarot Tips for Beginners", "category": "Tarot & Oracle"},
            {"title": "Mars Retrograde Explained: What It Means For You", "category": "Astrology"},
            {"title": "Understanding the Major Arcana: A Deep Dive", "category": "Tarot & Oracle"},
            {"title": "Moon Phases and Their Spiritual Significance", "category": "Spiritual Wellness"},
            {"title": "Meditation Techniques for Enhancing Psychic Abilities", "category": "Spiritual Wellness"}
        ]
        
        generated_posts = []
        for idea in blog_ideas:
            post_data = generate_blog_post(idea["title"], idea["category"])
            
            new_post = {
                "id": str(datetime.now().timestamp()),
                "title": idea["title"],
                "author": "AI Mystic",
                "date": datetime.now().strftime("%b %d, %Y"),
                "category": idea["category"],
                "content": post_data["content"],
                "ai_generated": True
            }
            
            generated_posts.append(new_post)
            
            # Add a small delay to avoid overwhelming the API
            import time
            time.sleep(2)
        
        # Add the generated posts to the database
        if 'blog_posts' not in db:
            db['blog_posts'] = SAMPLE_POSTS
        
        db['blog_posts'].extend(generated_posts)
        
        flash(f'Successfully generated {len(generated_posts)} blog posts', 'success')
        return redirect(url_for('blog.blog_home'))
    
    return render_template('generate_batch.html')
