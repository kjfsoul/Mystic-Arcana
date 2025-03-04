
import os
import openai
import json
from replit import db

# Initialize OpenAI client
openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_completion(prompt, max_tokens=1000):
    """
    Generate a completion using OpenAI's ChatGPT model
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in mysticism, tarot reading, and astrology."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating completion: {e}")
        return "The cosmic energies are too strong to connect at the moment. Please try again later."

def generate_tarot_reading(question, num_cards=3):
    """
    Generate a detailed tarot reading based on a question
    """
    from blueprints.readings import TAROT_CARDS
    import random
    
    # Select random cards for the reading
    cards = random.sample(TAROT_CARDS, num_cards)
    cards_info = ", ".join([f"{card['name']} ({card['meaning']})" for card in cards])
    
    prompt = f"""
    Generate a detailed tarot card reading for the following question: "{question}"
    
    The cards drawn are:
    {cards_info}
    
    Provide a thorough interpretation of each card in this specific context, 
    their relationships to each other, and an overall insight.
    Format your response in clear paragraphs with HTML formatting.
    """
    
    reading = generate_completion(prompt, max_tokens=1500)
    
    # Store the results in the database
    if 'ai_readings' not in db:
        db['ai_readings'] = []
    
    reading_entry = {
        "question": question,
        "cards": [card["name"] for card in cards],
        "reading": reading,
        "timestamp": import_datetime().now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    db['ai_readings'].append(reading_entry)
    return {"cards": cards, "reading": reading}

def generate_astrology_insight(zodiac_sign):
    """
    Generate a personalized astrology insight for a specific zodiac sign
    """
    prompt = f"""
    Generate a detailed daily horoscope for {zodiac_sign}. 
    Include insights about love, career, and personal growth.
    Focus on current celestial patterns and their influence.
    Format your response in clear paragraphs with HTML formatting.
    """
    
    insight = generate_completion(prompt, max_tokens=1000)
    
    # Store in database
    if 'ai_horoscopes' not in db:
        db['ai_horoscopes'] = {}
    
    db['ai_horoscopes'][zodiac_sign.lower()] = {
        "content": insight,
        "generated_at": import_datetime().now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return insight

def generate_blog_post(topic, category):
    """
    Generate a complete blog post on a mystical topic
    """
    prompt = f"""
    Generate a detailed blog post about "{topic}" for the category "{category}".
    The blog should be informative, engaging, and well-structured with:
    - An attention-grabbing introduction
    - 3-4 main sections with subheadings
    - Practical advice or insights
    - A thoughtful conclusion
    
    Format with HTML tags (<h3> for subheadings, <p> for paragraphs).
    Total length should be 800-1000 words.
    
    Use SEO best practices with:
    - Natural keyword placement
    - Short paragraphs (3-4 sentences)
    - Engaging subheadings
    - Include a meta description of 150-160 characters
    """
    
    content = generate_completion(prompt, max_tokens=2500)
    
    return {
        "title": topic,
        "category": category,
        "content": content,
        "timestamp": import_datetime().now().strftime("%Y-%m-%d %H:%M:%S")
    }

def generate_celtic_cross_reading(question):
    """
    Generate a detailed Celtic Cross spread reading (10 cards)
    """
    from blueprints.readings import TAROT_CARDS
    import random
    
    # Select 10 random cards for the Celtic Cross spread
    cards = random.sample(TAROT_CARDS, 10)
    
    positions = [
        "Present", "Challenge", "Past", "Future", 
        "Above (Conscious)", "Below (Unconscious)", 
        "Advice", "External Influences", 
        "Hopes/Fears", "Outcome"
    ]
    
    cards_info = ""
    for i, (card, position) in enumerate(zip(cards, positions)):
        cards_info += f"{i+1}. {position}: {card['name']} ({card['meaning']})\n"
    
    prompt = f"""
    Generate a detailed Celtic Cross tarot reading for the question: "{question}"
    
    The cards drawn are:
    {cards_info}
    
    Include an explanation of each card position in the Celtic Cross spread.
    Then provide a thorough interpretation of each card in its position.
    Finally, synthesize the cards into a cohesive reading that addresses the question.
    
    Format your response in clear paragraphs with HTML formatting, using 
    <h3> tags for sections and <p> for paragraphs.
    """
    
    reading = generate_completion(prompt, max_tokens=2000)
    
    return {"cards": cards, "reading": reading}

def generate_detailed_reading(question, cards=5):
    """
    Generate a detailed reading with a specific number of cards
    """
    from blueprints.readings import TAROT_CARDS
    import random
    
    # Select random cards for the reading
    selected_cards = random.sample(TAROT_CARDS, cards)
    
    cards_info = ""
    for i, card in enumerate(selected_cards):
        cards_info += f"{i+1}. {card['name']} ({card['meaning']})\n"
    
    prompt = f"""
    Generate a detailed tarot reading for the following question: "{question}"
    
    The {cards} cards drawn are:
    {cards_info}
    
    Provide a thorough interpretation of each card and its position in the spread.
    Explain how the cards relate to each other and create a narrative.
    Conclude with specific insights and guidance related to the question.
    
    Format your response in clear paragraphs with HTML formatting,
    using <h3> tags for each card's section and <p> for paragraphs.
    """
    
    reading = generate_completion(prompt, max_tokens=1800)
    
    return {"cards": selected_cards, "reading": reading}

def generate_seo_optimized_blog_posts():
    """
    Generate 5 SEO-optimized blog posts about mystical topics
    """
    blog_topics = [
        {
            "title": "The Seven-Planet Alignment of February 2025: A Cosmic Must-Know",
            "category": "Astrology", 
            "keywords": "planet alignment, February 2025, astrological significance, rare celestial event"
        },
        {
            "title": "Integrating Tarot and Oracle Cards for Deeper Readings",
            "category": "Tarot & Oracle",
            "keywords": "tarot, oracle cards, card reading techniques, spiritual guidance"
        },
        {
            "title": "Ancient Moon Rituals for Modern Self-Care Practices",
            "category": "Spiritual Wellness",
            "keywords": "moon rituals, self-care, lunar phases, spiritual practices"
        },
        {
            "title": "Understanding Your Natal Chart: Beyond Sun Signs",
            "category": "Astrology",
            "keywords": "natal chart, birth chart, planets, houses, aspects, astrology basics"
        },
        {
            "title": "The Hidden Wisdom of the Minor Arcana in Tarot",
            "category": "Tarot & Oracle",
            "keywords": "minor arcana, tarot suits, pentacles, cups, swords, wands, tarot meanings"
        }
    ]
    
    generated_posts = []
    
    for topic in blog_topics:
        prompt = f"""
        Generate a detailed blog post about "{topic['title']}" for the category "{topic['category']}".
        Keywords to include naturally: {topic['keywords']}
        
        The blog should follow SEO best practices with:
        - A compelling meta description (150-160 characters)
        - An attention-grabbing introduction with the primary keyword
        - 3-4 main sections with descriptive H2 subheadings
        - Short, scannable paragraphs (3-4 sentences)
        - Bullet points or numbered lists where appropriate
        - A clear call-to-action conclusion
        
        Format with HTML tags (<h3> for subheadings, <p> for paragraphs, <ul>/<li> for lists).
        Total length should be 1000-1500 words.
        
        Also include a meta description in a <meta_description> tag at the beginning.
        """
        
        content = generate_completion(prompt, max_tokens=3000)
        
        # Extract meta description if present
        meta_description = ""
        if "<meta_description>" in content and "</meta_description>" in content:
            start = content.find("<meta_description>") + len("<meta_description>")
            end = content.find("</meta_description>")
            meta_description = content[start:end].strip()
            content = content.replace(content[start-len("<meta_description>"):end+len("</meta_description>")], "")
        
        post = {
            "title": topic["title"],
            "category": topic["category"],
            "content": content,
            "meta_description": meta_description,
            "keywords": topic["keywords"],
            "author": "AI Mystic",
            "date": import_datetime().now().strftime("%b %d, %Y"),
            "timestamp": import_datetime().now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        generated_posts.append(post)
    
    return generated_posts

def import_datetime():
    """Helper function to avoid circular imports"""
    from datetime import datetime
    return datetime
