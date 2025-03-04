
from replit import db
from datetime import datetime
import hashlib
import os

def hash_password(password):
    salt = os.environ.get('PASSWORD_SALT', 'mystic_arcana_salt')
    return hashlib.sha256((password + salt).encode()).hexdigest()

def init_db():
    # Clear existing data
    for key in db.keys():
        del db[key]
    
    # Create admin user
    admin_id = "admin_user"
    db['users'] = {
        admin_id: {
            'id': admin_id,
            'name': 'Admin User',
            'email': 'admin@mysticarcana.com',
            'password': hash_password('admin123'),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'preferences': {
                'zodiac_sign': 'leo',
                'notifications': True
            }
        }
    }
    
    # Sample blog posts
    db['blog_posts'] = [
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
    
    print("Database initialized with sample data!")
    print("Admin login: admin@mysticarcana.com / admin123")

if __name__ == "__main__":
    init_db()
