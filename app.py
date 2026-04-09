from flask import Flask, render_template, request, redirect, url_for
import os
from db import db, cursor
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------------
# Home page - list posts
# ---------------------
@app.route('/')
def index():
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

# ---------------------
# Create post page
# ---------------------
@app.route('/create')
def create():
    return render_template('create.html')

# ---------------------
# Add new post
# ---------------------
@app.route('/add', methods=['POST'])
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files.get('image')

    filename = None
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    query = "INSERT INTO posts (title, content, image) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, content, filename))
    db.commit()
    return redirect(url_for('index'))

# ---------------------
# Delete post
# ---------------------
@app.route('/delete/<int:id>')
def delete_post(id):
    cursor.execute("DELETE FROM posts WHERE id=%s", (id,))
    db.commit()
    return redirect(url_for('index'))

# ---------------------
# Run server
# ---------------------
if __name__ == "__main__":
    app.run(debug=True)