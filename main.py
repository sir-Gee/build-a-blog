from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:qwerty@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.String(255))

    def __init__(self, title, text):
        self.title = title
        self.text = text


@app.route('/addpost', methods=['POST', 'GET'])
def add_post():

    post_title = ''
    post_text = ''

    if request.method == 'POST':
        post_title = request.form['title']
        post_text = request.form['text']

        if post_title == Blog.query.filter_by(title=post_title).first():
            return redirect("/addpost?error=You have this post already")

        if len(post_title) == 0 or len(post_text) == 0:
            flash('Error: Title or body can\'t be empty')

            return render_template('addpost.html', entered_post=post_text, entered_title=post_title)

        blog = Blog(post_title, post_text)
        db.session.add(blog)
        db.session.commit()

        return redirect("/?post_title={title}".format(title=blog.title))

    return render_template('addpost.html', entered_post=post_text, entered_title=post_title)


@app.route('/', methods=['POST', 'GET'])
def index():

    post_title = request.args.get('post_title')

    if post_title:
        blog = Blog.query.filter_by(title=post_title).first()
        return render_template('post.html', post=blog)

    all_posts = Blog.query.all()

    return render_template('posts.html', title="Build a blog!", posts=all_posts)


def is_email(string):
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == '__main__':
    app.run()
