from flask import Flask, render_template, request, jsonify, redirect, url_for
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

from models import User, Post, Comment

# @app.route("/", methods=["GET", "POST"])
# def hello_world():
#    marks = {
#       "Math": 90,
#       "Science": 85,
#       "History": 92
#    }
#    return render_template("index.html", marks=marks)
@app.route("/", methods=["GET", "POST"])
def hello_world():

   return render_template("pages/index.html")

@app.route('/populate')
def populate():
    # Create sample data to play with associations
    user1 = User(username='alice', email='alice@example.com')
    user2 = User(username='bob', email='bob@example.com')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    post1 = Post(title='First Post', content='This is the first post.', user_id=user1.id)
    post2 = Post(title='Second Post', content='This is the second post.', user_id=user2.id)
    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()

    comment1 = Comment(content='Great post!', post_id=post1.id, user_id=user2.id)
    comment2 = Comment(content='Thanks!', post_id=post1.id, user_id=user1.id)
    db.session.add(comment1)
    db.session.add(comment2)
    db.session.commit()

    return 'Database populated with sample data!'

@app.route('/data')
def get_data():
    users = User.query.all()
    posts = Post.query.all()
    comments = Comment.query.all()
    
    data = {
        'users': [{'id': u.id, 'username': u.username, 'email': u.email, 'posts_count': len(u.posts), 'comments_count': len(u.comments)} for u in users],
        'posts': [{'id': p.id, 'title': p.title, 'content': p.content, 'author': p.author.username, 'comments_count': len(p.comments)} for p in posts],
        'comments': [{'id': c.id, 'content': c.content, 'post_title': c.post.title, 'commenter': c.commenter.username} for c in comments]
    }
    
    return jsonify(data)

# Users CRUD
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users'))
    users_list = User.query.all()
    return render_template('pages/users.html', users=users_list)

@app.route('/user/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('pages/edit_user.html', user=user)

@app.route('/user/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

# Posts CRUD
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = request.form['user_id']
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    posts_list = Post.query.all()
    users_list = User.query.all()
    return render_template('pages/posts.html', posts=posts_list, users=users_list)

@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.user_id = request.form['user_id']
        db.session.commit()
        return redirect(url_for('posts'))
    users_list = User.query.all()
    return render_template('pages/edit_post.html', post=post, users=users_list)

@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts'))

# Comments CRUD
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        content = request.form['content']
        post_id = request.form['post_id']
        user_id = request.form['user_id']
        comment = Comment(content=content, post_id=post_id, user_id=user_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('comments'))
    comments_list = Comment.query.all()
    posts_list = Post.query.all()
    users_list = User.query.all()
    return render_template('pages/comments.html', comments=comments_list, posts=posts_list, users=users_list)

@app.route('/comment/<int:id>/edit', methods=['GET', 'POST'])
def edit_comment(id):
    comment = Comment.query.get_or_404(id)
    if request.method == 'POST':
        comment.content = request.form['content']
        comment.post_id = request.form['post_id']
        comment.user_id = request.form['user_id']
        db.session.commit()
        return redirect(url_for('comments'))
    posts_list = Post.query.all()
    users_list = User.query.all()
    return render_template('pages/edit_comment.html', comment=comment, posts=posts_list, users=users_list)

@app.route('/comment/<int:id>/delete', methods=['POST'])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('comments'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)