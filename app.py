from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/mypage")
def mypage():
    return render_template('mypage.html')

@app.route('/profile/<username>')
def profile(username):
    return f'{username}さんのプロフィールページ'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'投稿番号: {post_id}'

if __name__ == "__main__":
    app.run(debug=True)