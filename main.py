
from flask import Flask, render_template
import os

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/readings')
def readings():
    return render_template('readings.html')

@app.route('/astrology')
def astrology():
    return render_template('astrology.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
