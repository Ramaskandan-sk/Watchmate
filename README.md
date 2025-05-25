# Watchmate - Anime, Movie and Series Watchlist

A full-stack web application built with Flask and PostgreSQL/MySQL that allows users to create and manage watchlists for Movies, Anime, and Series. The application includes user authentication, a dashboard to view watchlist items with filtering, functionality to add new items, and a user profile page.

## Features

- User authentication (signup, login, logout)
- Password hashing for security
- Landing page with anime-themed design
- Dashboard with watchlist items displayed in a card layout
- Filter watchlist items by category (Movie, Anime, Series)
- Add new items to your watchlist with support for both URL and local images
- Delete items from your watchlist
- User profile page
- Responsive design with Bootstrap

## Setup Instructions

### Option 1: Using PostgreSQL (Replit or any cloud hosting)

1. Make sure the PostgreSQL connection string is set in the environment variable `DATABASE_URL`
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

### Option 2: Using MySQL (XAMPP for local development)

1. Install and start XAMPP
2. Start Apache and MySQL services
3. Create a database named `watchmate_db2`
4. Update the database connection string in `app.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/watchmate_db2'
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Run the application:
   ```
   python main.py
   ```

## Project Structure

- `app.py`: Main application file with routes and logic
- `models.py`: Database models for User and WatchlistItem
- `forms.py`: Form classes for user input
- `main.py`: Entry point for the application
- `templates/`: HTML templates for rendering pages
- `static/`: Static files (CSS, JavaScript, images)

## Using Local Images

You can add items to your watchlist using either:

1. URLs to online images
2. Local image paths in the format `img/image.jpg` or `static/img/image.jpg`

To use local images:

1. Place your images in the `static/img/` directory
2. When adding an item, specify the path as `img/filename.jpg` or `static/img/filename.jpg`

## Technologies Used

- Flask: Web framework
- Flask-Login: User session management
- Flask-SQLAlchemy: ORM for database interactions
- Flask-WTF: Form handling and validation
- Bootstrap: Frontend design
- PostgreSQL/MySQL: Database
- Werkzeug: Password hashing
