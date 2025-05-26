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
   pip install -r dependencies.txt
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
   pip install -r dependencies.txt
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

## 📸 Project Preview
![Image](https://github.com/user-attachments/assets/de15b6e8-9a6a-414d-9a98-7f4d2cf954a3)
![Image](https://github.com/user-attachments/assets/5c5d46d2-f884-447f-9f11-82fb132bc4db)
![Image](https://github.com/user-attachments/assets/32238ce0-e45a-4440-bb3c-d81bf3caa16a)
![Image](https://github.com/user-attachments/assets/8bd692fe-fc0e-44bd-b29a-c39579668e04)
![Image](https://github.com/user-attachments/assets/22bcbcac-75f6-4873-86ef-f1bf9aa58f64)
![Image](https://github.com/user-attachments/assets/5a15cb74-0cce-4ab8-96d4-13a142047102)
![Image](https://github.com/user-attachments/assets/9a3136cb-db29-41d1-bcc1-2774abb92c9f)

