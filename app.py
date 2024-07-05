from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from post import LinkedList
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"BlogPost {self.title}"

blog_posts = LinkedList()

@app.route('/')
def home():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    blog_posts = LinkedList()  # Reset the LinkedList
    for post in posts:
        blog_posts.insert(str(post.id), post.title, post.content, post.date)
    return render_template('blog.html', posts=blog_posts.traverse())

@app.route('/insert', methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        new_post = BlogPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        blog_posts.insert(str(new_post.id), title, content, new_post.date)
        return redirect(url_for('home'))
    return render_template('insert.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        blog_posts.update(str(id), post.title, post.content, post.date)
        return redirect(url_for('home'))
    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>')
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    blog_posts.delete(str(id))
    return redirect(url_for('home'))

@app.route('/post/<int:id>')
def view_post(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('post.html', post=post)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)