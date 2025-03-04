
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from replit import db
import os
import json
from datetime import datetime
from blueprints.home import home_bp
from blueprints.readings import readings_bp
from blueprints.astrology import astrology_bp
from blueprints.profile import profile_bp
from blueprints.blog import blog_bp

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

app.secret_key = os.environ.get('SECRET_KEY', 'mystic_arcana_secret_key')

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(readings_bp)
app.register_blueprint(astrology_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(blog_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
