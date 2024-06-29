
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from post import LinkedList
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
blog_posts = LinkedList()
db = SQLAlchemy(app)

class blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(2000), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"blogpost {self.title}"

@app.route('/')
def home():
    posts = blog_posts.traverse()
    return render_template('blog.html',posts=posts)

@app.route('/insert',methods=["GET", "POST"])
def create_post():
    if 'title' in request.form and 'content' in request.form:
            title = "request.form['title']"
            content = "request.form['content']"
            blogs = blogpost(title=title, content=content)
            db.session.add(blogs)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('insert.html')
'''
@app.route('/edit/<string:title>', methods=['GET', 'POST'])
def edit_post(title):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        blog_posts.update(title, new_title, new_content)
        return redirect(url_for('home'))
    else:
        current = blog_posts.head
        post = None
        while current and current.title != title:
            current = current.next
        if current:
            post = {'title': current.title, 'content': current.content}
        return render_template('edit.html', post=post)

@app.route('/delete/<string:title>')
def delete_post(title):
    blog_posts.delete(title)
    return redirect(url_for('home'))
'''
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

