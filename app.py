from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
from bson.objectid import ObjectId
from PIL import Image
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)  # Enable CORS for development

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['newsDB']
collection = db['articles']
users_collection = db['users']  # Collection for user accounts

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add authentication logic here
        if username == 'admin' and password == 'password':  # Replace with actual authentication
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

def get_ordinal_suffix(day):
    if 11 <= day <= 13:
        return 'th'
    elif day % 10 == 1:
        return 'st'
    elif day % 10 == 2:
        return 'nd'
    elif day % 10 == 3:
        return 'rd'
    else:
        return 'th'

def format_date_with_ordinal(date):
    day = date.day
    suffix = get_ordinal_suffix(day)
    return date.strftime(f'%B {day}{suffix} %Y')

@app.route('/')
def index():
    # Retrieve all articles from the database and sort by date in descending order
    articles = list(collection.find().sort('date', -1))
    for article in articles:
        if isinstance(article['date'], datetime):
            article['date'] = format_date_with_ordinal(article['date'])
    # Render the template with articles
    return render_template('index.html', articles=articles)

@app.route('/submit', methods=['GET'])
def submit_article_form():
    return render_template('submit_article.html')

def get_image_orientation(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        if width > height:
            return 'landscape'
        else:
            return 'portrait'

@app.route('/api/news')
def get_news():
    # Retrieve the top 5 most recent articles from the database
    news = list(collection.find().sort('date', -1).limit(5))
    for item in news:
        item['_id'] = str(item['_id'])
        if isinstance(item['date'], datetime):
            item['date'] = format_date_with_ordinal(item['date'])
    return jsonify(news)

@app.route('/submit_article', methods=['POST'])
def submit_article():
    title = request.form['title']
    date_str = request.form['date']
    author = request.form['author']
    category = request.form['category']
    content = request.form['content']
    image = request.form['image']

    # Parse the date from the form
    date = datetime.strptime(date_str, '%Y-%m-%d')

    # Insert the new article into MongoDB
    collection.insert_one({
        'title': title,
        'date': date,
        'author': author,
        'category': category,
        'content': content,
        'image': image
    })

    return redirect(url_for('index'))

@app.route('/article/<article_id>')
def article(article_id):
    article = collection.find_one({'_id': ObjectId(article_id)})
    if article:
        article['_id'] = str(article['_id'])
        if isinstance(article['date'], datetime):
            article['date'] = format_date_with_ordinal(article['date'])
        return render_template('article.html', article=article)
    return "Article not found", 404


@app.route('/staff')
def staff_display():
    return render_template('staff.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

@app.route('/add_account')
def add_account():
    return render_template('pages/add_account.html')

@app.route('/monitor_active_account')
def monitor_active_account():
    return "Monitor Active Accounts Page - Implement functionality here"

@app.route('/modify_active_account')
def modify_active_account():
    return "Modify Active Accounts Page - Implement functionality here"

@app.route('/settings')
def settings_account():
    return render_template('pages/accountsettings.html')

if __name__ == '__main__':
    app.run(debug=True)
