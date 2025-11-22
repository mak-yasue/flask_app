import os
from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/mypage")
def mypage():
    return render_template('mypage.html')

@app.route("/information")
def information():
    return render_template('information.html')

@app.route('/profile/<username>')
def profile(username):
    age = 19
    hobbies = ['プログラミング', '音楽', '映画鑑賞','スポーツ','ギャンブル']
    gender = '男'
    return render_template('profile.html', username=username, age=age, hobbies=hobbies, gender=gender)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'投稿番号: {post_id}'

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    hobby = request.form['hobby']
    error = None

    if not name or not age:
        error = '全ての項目を入力してください'
    
    return render_template('result.html', name=name, age=age, hobby=hobby, error=error)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return 'ファイルが選択されていません'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            return '許可されていないファイル形式です'
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'アップロード完了: <br><img src="/static/uploads/{filename}" width="300">'

@app.route('/gallery')
def gallery():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', images=images)

if __name__ == "__main__":
    app.run(debug=True)
    
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)

# ==========================
# 初回起動 以下を処理する場合は、「python app.py」で実行する
# ==========================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        user = User(name=name, age=age)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('register.html')

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)
