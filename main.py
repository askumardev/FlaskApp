from flask import Flask, render_template, request, jsonify, redirect, url_for
from db import db
from uuid import UUID

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

from models import User, Post, Comment, Category
from api import api_bp

app.register_blueprint(api_bp)

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
    # Create sample data to play with associations (idempotent)
    user1 = User.query.filter_by(email='alice@example.com').first()
    if not user1:
        user1 = User(username='alice', email='alice@example.com')
        db.session.add(user1)

    user2 = User.query.filter_by(email='bob@example.com').first()
    if not user2:
        user2 = User(username='bob', email='bob@example.com')
        db.session.add(user2)

    db.session.commit()

    # category sample
    cat_general = Category.query.filter_by(name='General').first()
    if not cat_general:
        cat_general = Category(name='General', description='General category')
        db.session.add(cat_general)

    cat_news = Category.query.filter_by(name='News').first()
    if not cat_news:
        cat_news = Category(name='News', description='Latest news updates')
        db.session.add(cat_news)

    cat_tutorial = Category.query.filter_by(name='Tutorial').first()
    if not cat_tutorial:
        cat_tutorial = Category(name='Tutorial', description='Tutorial and how-to guides')
        db.session.add(cat_tutorial)

    db.session.commit()

    post1 = Post.query.filter_by(title='First Post').first()
    if not post1:
        post1 = Post(title='First Post', content='This is the first post.', user_id=user1.id, category_id=cat_general.id)
        db.session.add(post1)

    post2 = Post.query.filter_by(title='Second Post').first()
    if not post2:
        post2 = Post(title='Second Post', content='This is the second post.', user_id=user2.id, category_id=cat_general.id)
        db.session.add(post2)

    db.session.commit()

    comment1 = Comment.query.filter_by(content='Great post!').first()
    if not comment1:
        comment1 = Comment(content='Great post!', post_id=post1.id, user_id=user2.id)
        db.session.add(comment1)

    comment2 = Comment.query.filter_by(content='Thanks!').first()
    if not comment2:
        comment2 = Comment(content='Thanks!', post_id=post1.id, user_id=user1.id)
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
@app.route('/users')
def users_index():
    users_list = User.query.all()
    return render_template('pages/users/index.html', users=users_list)

@app.route('/users/new', methods=['GET', 'POST'])
def users_new():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users_index'))
    return render_template('pages/users/new.html', user=None, button_text='Create User')

@app.route('/users/<int:id>')
def users_show(id):
    user = User.query.get_or_404(id)
    return render_template('pages/users/show.html', user=user)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def users_edit(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('users_index'))
    return render_template('pages/users/edit.html', user=user, button_text='Update User')

@app.route('/users/<int:id>/delete', methods=['POST'])
def users_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_index'))


# *******************************************************************************
# this route is just to show dynamic routing with a parameter, not part of CRUD
# localhost:8000/user/raju
@app.route('/user/<name>')
def user(name):
    return f"Hello, {name}!"

# this route is just to show dynamic routing with multiple parameters, not part of CRUD
# localhost:8000/student/raju/flask
@app.route('/student/<name>/<course>')
def student(name, course):
    return f"Hello, {name}! You are enrolled in {course}."
#if parammeter is not provided, it will show 404 error
# Not Found
# The requested URL was not found on the server. 
# If you entered the URL manually please check your spelling and try again.

# Accpting integer parameter
@app.route('/article/<int:id>')
def article(id):
    return f"Article Id is: {id}."

# Accpting float parameter
@app.route('/price/<float:amount>')
def price(amount):
    return f"Price is: ${amount}."

# Accpting string parameter
@app.route('/product/<string:name>')
def product(name):
    return f"Product is: {name}."

# path converter for file path, it will accept any text including slashes
@app.route('/files/<path:file_name>')
def files(file_name):
    return f"File is: {file_name}."

# uuid converter for UUID, it will accept only valid UUIDs
# http://127.0.0.1:8000/admin/3f8c2b6e-7a4d-4e9b-bc3a-8f2f9d4a1c7e
@app.route('/admin/<uuid:uuid_str>')
def admin(uuid_str):
    return f"Admin UUID is: {uuid_str}."

# *******************************************************************************

# Posts CRUD
@app.route('/posts')
def posts_index():
    posts_list = Post.query.all()
    return render_template('pages/posts/index.html', posts=posts_list)

@app.route('/posts/new', methods=['GET', 'POST'])
def posts_new():
    users_list = User.query.all()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = request.form['user_id']
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts_index'))
    return render_template('pages/posts/new.html', post=None, users=users_list, button_text='Create Post')

@app.route('/posts/<int:id>')
def posts_show(id):
    post = Post.query.get_or_404(id)
    return render_template('pages/posts/show.html', post=post)

@app.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
def posts_edit(id):
    post = Post.query.get_or_404(id)
    users_list = User.query.all()
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.user_id = request.form['user_id']
        db.session.commit()
        return redirect(url_for('posts_index'))
    return render_template('pages/posts/edit.html', post=post, users=users_list, button_text='Update Post')

@app.route('/posts/<int:id>/delete', methods=['POST'])
def posts_delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts_index'))

# Comments CRUD
@app.route('/comments')
def comments_index():
    comments_list = Comment.query.all()
    return render_template('pages/comments/index.html', comments=comments_list)

@app.route('/comments/new', methods=['GET', 'POST'])
def comments_new():
    posts_list = Post.query.all()
    users_list = User.query.all()
    if request.method == 'POST':
        content = request.form['content']
        post_id = request.form['post_id']
        user_id = request.form['user_id']
        comment = Comment(content=content, post_id=post_id, user_id=user_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('comments_index'))
    return render_template('pages/comments/new.html', comment=None, posts=posts_list, users=users_list, button_text='Create Comment')

@app.route('/comments/<int:id>')
def comments_show(id):
    comment = Comment.query.get_or_404(id)
    return render_template('pages/comments/show.html', comment=comment)

@app.route('/comments/<int:id>/edit', methods=['GET', 'POST'])
def comments_edit(id):
    comment = Comment.query.get_or_404(id)
    posts_list = Post.query.all()
    users_list = User.query.all()
    if request.method == 'POST':
        comment.content = request.form['content']
        comment.post_id = request.form['post_id']
        comment.user_id = request.form['user_id']
        db.session.commit()
        return redirect(url_for('comments_index'))
    return render_template('pages/comments/edit.html', comment=comment, posts=posts_list, users=users_list, button_text='Update Comment')

@app.route('/comments/<int:id>/delete', methods=['POST'])
def comments_delete(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('comments_index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Schema evolution: add post.category_id if missing
        try:
            db.session.execute('SELECT category_id FROM post LIMIT 1')
        except Exception:
            try:
                db.session.execute('ALTER TABLE post ADD COLUMN category_id INTEGER')
                db.session.commit()
                print('Migrated: added category_id column to post')
            except Exception as e:
                print('Migration ignored (maybe already present or unsupported):', str(e))
    app.run(port=8000, debug=True)