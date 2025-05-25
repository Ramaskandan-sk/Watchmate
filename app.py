import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import SignupForm, LoginForm, AddWatchlistItemForm, EditWatchlistItemForm
from models import db, User, WatchlistItem

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure SQLAlchemy with PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:@localhost:3306/watchmate_db2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True
}

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for home page
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = SignupForm()
    if form.validate_on_submit():
        # Get form data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return render_template('signup.html', form=form)
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
            return render_template('signup.html', form=form)
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Create new user
        new_user = User(username=username, email=email, password=hashed_password)
        
        # Add user to database
        db.session.add(new_user)
        db.session.commit()
        
        # Flash message
        flash('You are now registered and can log in', 'success')
        
        # Redirect to login page
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Get form data
        username = form.username.data
        password_candidate = form.password.data
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if user:
            # Compare passwords
            if check_password_hash(user.password, password_candidate):
                # Log in user with Flask-Login
                login_user(user)
                
                flash('You are now logged in', 'success')
                
                # Redirect to requested page or dashboard
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Invalid login credentials', 'danger')
                return render_template('login.html', form=form)
        else:
            flash('Username not found', 'danger')
            return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)

# Route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Route for dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Get category filter
    category = request.args.get('category', '')
    
    # Get watchlist items using SQLAlchemy
    if category:
        watchlist = WatchlistItem.query.filter_by(user_id=current_user.id, category=category).order_by(WatchlistItem.id.desc()).all()
    else:
        watchlist = WatchlistItem.query.filter_by(user_id=current_user.id).order_by(WatchlistItem.id.desc()).all()
    
    return render_template('dashboard.html', watchlist=watchlist, category=category)

# Route for adding watchlist item
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddWatchlistItemForm()
    if form.validate_on_submit():
        # Get form data
        title = form.title.data
        image_url = form.image_url.data
        category = form.category.data
        
        # Create new watchlist item
        new_item = WatchlistItem(user_id=current_user.id, title=title, image_url=image_url, category=category)
        
        # Add to database
        db.session.add(new_item)
        db.session.commit()
        
        flash('Item added to watchlist', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add.html', form=form)

# Route for editing watchlist item
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    # Find the item
    item = WatchlistItem.query.get_or_404(item_id)
    
    # Check if the item belongs to the current user
    if item.user_id != current_user.id:
        flash('You are not authorized to edit this item', 'danger')
        return redirect(url_for('dashboard'))
    
    form = EditWatchlistItemForm()
    
    if request.method == 'GET':
        # Pre-populate form with existing data
        form.title.data = item.title
        form.image_url.data = item.image_url
        form.category.data = item.category
    
    if form.validate_on_submit():
        # Update item data
        item.title = form.title.data
        item.image_url = form.image_url.data
        item.category = form.category.data
        
        # Save to database
        db.session.commit()
        
        flash('Item updated successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit.html', form=form, item=item)

# Route for profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# API endpoint for watchlist
@app.route('/watchlist')
@login_required
def get_watchlist():
    # Get category filter
    category = request.args.get('category', '')
    
    # Get watchlist items using SQLAlchemy
    if category:
        watchlist = WatchlistItem.query.filter_by(user_id=current_user.id, category=category).order_by(WatchlistItem.id.desc()).all()
    else:
        watchlist = WatchlistItem.query.filter_by(user_id=current_user.id).order_by(WatchlistItem.id.desc()).all()
    
    # Convert to list of dictionaries for JSON response
    result = [{
        'id': item.id,
        'title': item.title,
        'image_url': item.image_url,
        'category': item.category,
        'created_at': item.created_at.isoformat() if item.created_at else None
    } for item in watchlist]
    
    return jsonify(result)

# Route for deleting watchlist item
@app.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    # Find the item
    item = WatchlistItem.query.get_or_404(item_id)
    
    # Check if the item belongs to the current user
    if item.user_id != current_user.id:
        flash('You are not authorized to delete this item', 'danger')
        return redirect(url_for('dashboard'))
    
    # Delete the item
    db.session.delete(item)
    db.session.commit()
    
    flash('Item deleted successfully', 'success')
    return redirect(url_for('dashboard'))

# Route for importing watchlist items
@app.route('/import_watchlist', methods=['POST'])
@login_required
def import_watchlist():
    try:
        # Get JSON data from request
        data = request.json
        items = data.get('items', [])
        
        if not items:
            return jsonify({'success': False, 'error': 'No items provided'})
        
        # Validate items
        valid_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
                
            title = item.get('title')
            image_url = item.get('image_url')
            category = item.get('category')
            
            if not title or not image_url or not category:
                continue
                
            # Validate category
            if category not in ['Movie', 'Anime', 'Series']:
                # Try to normalize category
                category_lower = category.lower()
                if 'movie' in category_lower:
                    category = 'Movie'
                elif 'anime' in category_lower:
                    category = 'Anime'
                elif 'series' in category_lower or 'tv' in category_lower:
                    category = 'Series'
                else:
                    category = 'Movie'  # Default to Movie
            
            valid_items.append({
                'title': title,
                'image_url': image_url,
                'category': category
            })
        
        if not valid_items:
            return jsonify({'success': False, 'error': 'No valid items found in import file'})
        
        # Add items to database
        for item_data in valid_items:
            new_item = WatchlistItem(
                user_id=current_user.id,
                title=item_data['title'],
                image_url=item_data['image_url'],
                category=item_data['category']
            )
            db.session.add(new_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'count': len(valid_items),
            'message': f'Successfully imported {len(valid_items)} items'
        })
        
    except Exception as e:
        print(f"Import error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

# Initialize database
def init_db():
    with app.app_context():
        try:
            db.create_all()
            logging.debug("Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")
            raise

# Initialize database when app starts
with app.app_context():
    try:
        init_db()
        logging.debug("Database initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        print(f"Database Error: {e}")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting Flask app: {e}")