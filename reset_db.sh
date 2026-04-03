#!/bin/bash

# Reset script for FlaskApp SQLite database
# Usage: bash reset_db.sh

set -e

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$WORKDIR"

DB_FILE="site.db"

echo "Stopping if any app is running..."
# user should manually stop app if running

if [ -f "$DB_FILE" ]; then
  echo "Removing existing database file: $DB_FILE"
  rm -f "$DB_FILE"
else
  echo "No existing database file found."
fi

# Create DB and tables using Flask app
echo "Creating database and tables..."
python3 - <<'PY'
from main import app, db
from sqlalchemy import text
with app.app_context():
    db.create_all()
    # Schema evolution: add post.category_id if missing
    try:
        db.session.execute(text('SELECT category_id FROM post LIMIT 1'))
    except Exception:
        try:
            db.session.execute(text('ALTER TABLE post ADD COLUMN category_id INTEGER'))
            db.session.commit()
            print('Migrated: added category_id column to post')
        except Exception as e:
            print('Migration ignored (maybe already present or unsupported):', str(e))
    print('DB schema created.')
PY

# Seed data using /populate route
echo "Seeding sample data..."
python3 - <<'PY'
from main import app, db
from models import User, Post, Comment, Category
with app.app_context():
    # Run the same seed function manually
    user1 = User.query.filter_by(email='alice@example.com').first()
    if not user1:
        user1 = User(username='alice', email='alice@example.com')
        db.session.add(user1)

    user2 = User.query.filter_by(email='bob@example.com').first()
    if not user2:
        user2 = User(username='bob', email='bob@example.com')
        db.session.add(user2)

    db.session.commit()

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
    print('Seed data inserted.')
PY

echo "Database reset and seed complete."

echo "Database reset and seed complete."
