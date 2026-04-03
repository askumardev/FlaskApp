# Flask-SQLAlchemy Query Reference

This reference shows common queries you can run from Flask routes or shell using SQLAlchemy models (`User`, `Post`, `Comment`).

## 1. Basic retrieval

- `all()` - get all records
  ```python
  users = User.query.all()
  posts = Post.query.all()
  comments = Comment.query.all()
  ```

- `get(id)` - get by primary key
  ```python
  user = User.query.get(1)
  post = Post.query.get(2)
  ```

- `get_or_404(id)` (in route, raise 404 on miss)
  ```python
  post = Post.query.get_or_404(post_id)
  ```

- `first()` - get first row or None
  ```python
  first_user = User.query.first()
  ```

- `filter_by(field=value)` - equality shortcuts
  ```python
  alice = User.query.filter_by(username='alice').first()
  bob_posts = Post.query.filter_by(user_id=2).all()
  ```

- `filter(<criteria>)` - SQL expression with operators
  ```python
  from sqlalchemy import or_

  users_like_a = User.query.filter(User.username.ilike('a%')).all()
  recent_posts = Post.query.filter(Post.id > 100).all()
  combined = User.query.filter(or_(User.username=='alice', User.username=='bob')).all()
  ```

## 2. Ordering and limiting

- `order_by()`
  ```python
  latest_posts = Post.query.order_by(Post.date_posted.desc()).all()
  oldest_users = User.query.order_by(User.username.asc()).all()
  ```

- `limit()` and `offset()`
  ```python
  five_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
  page2 = Post.query.order_by(Post.id).offset(5).limit(5).all()
  ```

## 3. Counting and existence

- `count()`
  ```python
  total_users = User.query.count()
  bob_comments = Comment.query.filter_by(user_id=2).count()
  ```

- `exists()`
  ```python
  from sqlalchemy.sql import exists

  has_posts = db.session.query(exists().where(Post.user_id == 1)).scalar()
  ```

## 4. Aggregation

- `func` (SQL functions)
  ```python
  from sqlalchemy import func

  user_count = db.session.query(func.count(User.id)).scalar()
  max_posts = db.session.query(func.max(Post.id)).scalar()
  ```

- group by
  ```python
  counts_per_user = db.session.query(User.username, func.count(Post.id).label('post_count')).join(Post).group_by(User.id).all()
  ```

## 5. Relationships and eager loading

- One-to-many via model attributes
  ```python
  user = User.query.get(1)
  user_posts = user.posts  # list of Post objects
  ```

- Lazy load vs join
  ```python
  from sqlalchemy.orm import joinedload

  posts_with_user = Post.query.options(joinedload(Post.author)).all()
  for p in posts_with_user:
      print(p.author.username)
  ```

- filter on joined relationship
  ```python
  posts_by_alice = Post.query.join(User).filter(User.username == 'alice').all()
  ```

## 6. Insert, update, delete

- Insert
  ```python
  new_user = User(username='charlie', email='charlie@example.com')
  db.session.add(new_user)
  db.session.commit()
  ```

- Update
  ```python
  user = User.query.get(3)
  user.email = 'newemail@example.com'
  db.session.commit()
  ```

- Delete
  ```python
  user = User.query.get(3)
  db.session.delete(user)
  db.session.commit()
  ```

## 7. Bulk operations

- `update()` and `delete()` (careful with side effects)
  ```python
  Post.query.filter(Post.user_id == 2).update({'title': 'Updated Title'}, synchronize_session='fetch')
  db.session.commit()

  Comment.query.filter(Comment.post_id == 1).delete(synchronize_session='fetch')
  db.session.commit()
  ```

## 8. Utility commands (shell)

Run inside shell with app context:

```bash
source .env
flask shell
```

Then in interactive shell:

```python
from main import db, User, Post, Comment
User.query.all()
post = Post.query.first()
post.content = 'Updated content'
db.session.commit()

# To print routes and endpoints:
from main import app
print(app.url_map)
```

---

This file is your query cheat sheet for CRUD and advanced patterns in Flask-SQLAlchemy.