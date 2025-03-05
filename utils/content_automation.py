
import os
import openai
from replit import db
from datetime import datetime
from utils.openai_client import generate_tarot_reading, generate_astrology_insight

def generate_daily_content():
    """Generate fresh content for the daily tarot reading and horoscopes"""
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Generating content for {today}")
    
    # 1. Generate daily tarot reading
    try:
        ai_result = generate_tarot_reading("What energies are present for everyone today?")
        
        if 'daily_readings' not in db:
            db['daily_readings'] = {}
        
        db['daily_readings'][today] = {
            "date": today,
            "cards": ai_result["cards"],
            "reading": ai_result["reading"]
        }
        print(f"✅ Daily tarot reading generated successfully")
    except Exception as e:
        print(f"❌ Error generating daily tarot reading: {e}")
    
    # 2. Generate general cosmic insight for today
    try:
        from utils.openai_client import generate_completion
        prompt = f"""
        Generate a short general astrological insight for today ({today}).
        Focus on overall cosmic energy, lunar phase, and meaningful transits.
        Keep it under 250 words and format with basic HTML.
        """
        general_insight = generate_completion(prompt, max_tokens=500)
        
        if 'daily_horoscopes' not in db:
            db['daily_horoscopes'] = {}
        
        db['daily_horoscopes'][today] = {
            "date": today,
            "general_insight": general_insight
        }
        print(f"✅ Daily cosmic insight generated successfully")
    except Exception as e:
        print(f"❌ Error generating daily cosmic insight: {e}")
    
    # 3. Generate horoscopes for all zodiac signs
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    for sign in zodiac_signs:
        try:
            horoscope_text = generate_astrology_insight(sign)
            
            # Store the generated horoscope in the database
            if 'zodiac_horoscopes' not in db:
                db['zodiac_horoscopes'] = {}
            
            if today not in db['zodiac_horoscopes']:
                db['zodiac_horoscopes'][today] = {}
                
            db['zodiac_horoscopes'][today][sign.lower()] = horoscope_text
            
            print(f"✅ Generated horoscope for {sign}")
            # Add a small delay to avoid API rate limits
            import time
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error generating horoscope for {sign}: {e}")
    
    print("🌟 Daily content generation completed")

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    generate_daily_content()
