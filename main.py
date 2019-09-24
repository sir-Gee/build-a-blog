from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:qwerty@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_text = db.Column(db.String(255))

    def __init__(self, post_text):
        self.post_text = post_text


all_posts = []


@app.route('/addpost', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        post = request.form['new-post-text']

    return render_template('base.html')


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post = request.form['new-post-text']

        if post in all_posts:
            return redirect("/?error=You have this post already")

        db.session.add(Blog(str(post)))
        db.session.commit()
        results = db.session.execute(select([Blog]))
        all_posts.clear()
        for item in results:
            all_posts.append(item[1])

    if request.method == 'GET':
        results = db.session.execute(select([Blog]))
        all_posts.clear()
        for item in results:
            all_posts.append(item[1])

    return render_template('posts.html', title="Build a blog!", all_posts=all_posts, errorTask=request.args.get("error"))


if __name__ == '__main__':
    app.run()
