from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key_here"  # Add this line for flash messages
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"BlogPost {self.title}"

@app.route('/')
def home():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/post/<int:id>')
def view_post(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/insert', methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        new_post = BlogPost(title=title, content=content)
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))
        except:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    return render_template('insert.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('view_post', id=post.id))
    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>')
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)