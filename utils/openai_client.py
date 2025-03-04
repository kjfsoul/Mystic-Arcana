
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
    """
    
    content = generate_completion(prompt, max_tokens=2500)
    
    return {
        "title": topic,
        "category": category,
        "content": content,
        "timestamp": import_datetime().now().strftime("%Y-%m-%d %H:%M:%S")
    }

def import_datetime():
    """Helper function to avoid circular imports"""
    from datetime import datetime
    return datetime
