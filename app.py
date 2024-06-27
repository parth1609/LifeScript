from flask import Flask,render_template

from post import LinkedList

app = Flask(__name__)
blog_posts = LinkedList()


@app.route('/')
def home():
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)