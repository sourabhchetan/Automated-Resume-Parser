from flask import Flask, render_template, request, redirect, url_for
import os
from parser.extract_text import extract_text
from parser.parse_resume import parse_resume
import psycopg2
from config import DB_CONFIG

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DB Connection
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['resume']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            text = extract_text(filepath)
            data = parse_resume(text)

            # Insert into DB
            cursor.execute("""
                INSERT INTO candidates (name, email, phone, skills, education, resume_file)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data['name'], data['email'], data['phone'], data['skills'], data['education'], file.filename))
            conn.commit()

            return render_template('result.html', data=data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
