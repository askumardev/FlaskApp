# Flask App with SQLAlchemy Models and CRUD Operations

This is a Flask web application that demonstrates database models with relationships and full CRUD (Create, Read, Update, Delete) operations.

## Features

- **Database Models**: User, Post, and Comment with SQLAlchemy relationships
- **CRUD Operations**: Web pages for managing users, posts, and comments
- **Associations**: Users can have multiple posts and comments; Posts belong to users and have comments; Comments belong to posts and users
- **Sample Data**: Route to populate the database with sample data
- **Data View**: JSON endpoint to view all data and associations

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Run the Flask app:
   ```bash
   python main.py
   ```

2. Open your browser and go to `http://localhost:8000`

## URLs and Pages

### Main Pages
- **`/`** - Home page with navigation links
- **`/populate`** - Populate the database with sample data (users, posts, comments)
- **`/data`** - View all data as JSON (shows associations and counts)

### Users CRUD
- **`/users`** - List all users, add new user
- **`/user/<id>/edit`** - Edit a specific user
- **`/user/<id>/delete`** - Delete a specific user (POST request)

### Posts CRUD
- **`/posts`** - List all posts, add new post (select author)
- **`/post/<id>/edit`** - Edit a specific post (change title, content, author)
- **`/post/<id>/delete`** - Delete a specific post (POST request)

### Comments CRUD
- **`/comments`** - List all comments, add new comment (select post and commenter)
- **`/comment/<id>/edit`** - Edit a specific comment (change content, post, commenter)
- **`/comment/<id>/delete`** - Delete a specific comment (POST request)

## Database

- Uses SQLite (`site.db`) for simplicity
- Models are defined in `models.py`
- Database is created automatically on first run

## Models and Associations

- **User**: Has many posts and comments
- **Post**: Belongs to a user, has many comments
- **Comment**: Belongs to a post and a user

## File Structure

```
FlaskApp/
├── main.py              # Main Flask application
├── models.py            # Database models
├── db.py                # Database configuration
├── requirements.txt     # Python dependencies
├── site.db              # SQLite database (created on run)
├── templates/
│   ├── layouts/
│   │   └── base.html    # Base template
│   └── pages/
│       ├── index.html   # Home page
│       ├── users.html   # Users list and add form
│       ├── edit_user.html
│       ├── posts.html   # Posts list and add form
│       ├── edit_post.html
│       ├── comments.html # Comments list and add form
│       └── edit_comment.html
├── static/              # Static files (CSS, JS, images)
└── README.md            # This file
```

## Usage Example

1. Start the app
2. Visit `/populate` to add sample data
3. Visit `/users` to see users and add more
4. Visit `/posts` to see posts and add more
5. Visit `/comments` to see comments and add more
6. Use `/data` to view JSON data with association details

## Notes

- Delete operations include confirmation prompts
- Forms validate required fields
- The app runs on port 8000 in debug mode



```
localhost:8000/static/sample.pdf
```