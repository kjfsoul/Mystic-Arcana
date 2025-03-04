
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from replit import db
from datetime import datetime

astrology_bp = Blueprint('astrology', __name__, url_prefix='/astrology')

ZODIAC_SIGNS = {
    "aries": {"dates": "March 21 - April 19", "element": "Fire", "ruling_planet": "Mars"},
    "taurus": {"dates": "April 20 - May 20", "element": "Earth", "ruling_planet": "Venus"},
    "gemini": {"dates": "May 21 - June 20", "element": "Air", "ruling_planet": "Mercury"},
    "cancer": {"dates": "June 21 - July 22", "element": "Water", "ruling_planet": "Moon"},
    "leo": {"dates": "July 23 - August 22", "element": "Fire", "ruling_planet": "Sun"},
    "virgo": {"dates": "August 23 - September 22", "element": "Earth", "ruling_planet": "Mercury"},
    "libra": {"dates": "September 23 - October 22", "element": "Air", "ruling_planet": "Venus"},
    "scorpio": {"dates": "October 23 - November 21", "element": "Water", "ruling_planet": "Pluto"},
    "sagittarius": {"dates": "November 22 - December 21", "element": "Fire", "ruling_planet": "Jupiter"},
    "capricorn": {"dates": "December 22 - January 19", "element": "Earth", "ruling_planet": "Saturn"},
    "aquarius": {"dates": "January 20 - February 18", "element": "Air", "ruling_planet": "Uranus"},
    "pisces": {"dates": "February 19 - March 20", "element": "Water", "ruling_planet": "Neptune"}
}

DAILY_HOROSCOPES = {
    "aries": "Today is a great day for new beginnings. Your energy is high, and you can accomplish a lot if you stay focused.",
    "taurus": "Stability is key today. Focus on self-care and building your resources. A financial opportunity may arise.",
    "gemini": "Communication is highlighted today. Share your ideas and connect with others - valuable insights await.",
    "cancer": "Your intuition is especially strong today. Trust your gut feelings and take care of your emotional needs.",
    "leo": "Your creative energy is flowing. Express yourself boldly and don't be afraid to take center stage.",
    "virgo": "Details matter today. Your analytical skills will help you solve problems and improve systems.",
    "libra": "Harmony in relationships is important today. Find balance between your needs and others'.",
    "scorpio": "Transformation is in the air. Let go of what no longer serves you and embrace personal power.",
    "sagittarius": "Adventure calls! Explore new ideas, places, or philosophies that expand your horizons.",
    "capricorn": "Focus on long-term goals today. Your discipline and practical approach will bring success.",
    "aquarius": "Innovation is your strength today. Think outside the box and connect with like-minded people.",
    "pisces": "Your imagination is powerful today. Creative pursuits and spiritual practices are especially rewarding."
}

@astrology_bp.route('/')
def astrology_home():
    return render_template('astrology.html', zodiac_signs=ZODIAC_SIGNS)

@astrology_bp.route('/horoscope/<sign>')
def horoscope(sign):
    if sign.lower() not in ZODIAC_SIGNS:
        return redirect(url_for('astrology.astrology_home'))
    
    horoscope_text = DAILY_HOROSCOPES.get(sign.lower(), "Horoscope not available")
    sign_info = ZODIAC_SIGNS.get(sign.lower(), {})
    
    return render_template('horoscope.html', 
                          sign=sign.capitalize(), 
                          horoscope=horoscope_text,
                          sign_info=sign_info)

@astrology_bp.route('/planet-alignment')
def planet_alignment():
    return render_template('planet_alignment.html')
