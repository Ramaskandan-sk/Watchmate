#!/usr/bin/env python3
"""
Script to create sample user and test data for Watchmate application
"""
import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime
import uuid

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, WatchlistItem

def create_sample_data():
    """Create sample user and watchlist items"""
    with app.app_context():
        try:
            # Check if sample user already exists
            existing_user = User.query.filter_by(username='testuser').first()
            if existing_user:
                print("Sample user 'testuser' already exists!")
                print(f"User ID: {existing_user.id}")
                print(f"Email: {existing_user.email}")
                
                # Show existing watchlist items
                items = WatchlistItem.query.filter_by(user_id=existing_user.id).all()
                print(f"Existing watchlist items: {len(items)}")
                for item in items:
                    print(f"  - {item.title} ({item.category})")
                return existing_user
            
            # Create sample user
            sample_user = User(
                id=str(uuid.uuid4()),
                username='testuser',
                email='test@example.com',
                password=generate_password_hash('password123'),
                created_at=datetime.utcnow()
            )
            
            db.session.add(sample_user)
            db.session.commit()
            
            print("✅ Sample user created successfully!")
            print(f"Username: testuser")
            print(f"Email: test@example.com")
            print(f"Password: password123")
            print(f"User ID: {sample_user.id}")
            
            # Create sample watchlist items
            sample_items = [
                {
                    'title': 'Demon Slayer: Kimetsu no Yaiba',
                    'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400',
                    'category': 'Anime'
                },
                {
                    'title': 'Attack on Titan',
                    'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400',
                    'category': 'Anime'
                },
                {
                    'title': 'Inception',
                    'image_url': 'https://images.unsplash.com/photo-1489599735734-79b4169c2a78?w=400',
                    'category': 'Movie'
                },
                {
                    'title': 'The Dark Knight',
                    'image_url': 'https://images.unsplash.com/photo-1489599735734-79b4169c2a78?w=400',
                    'category': 'Movie'
                },
                {
                    'title': 'Breaking Bad',
                    'image_url': 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=400',
                    'category': 'Series'
                },
                {
                    'title': 'Stranger Things',
                    'image_url': 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=400',
                    'category': 'Series'
                },
                {
                    'title': 'Your Name',
                    'image_url': 'img/naruto.jpeg',
                    'category': 'Anime'
                },
                {
                    'title': 'Spirited Away',
                    'image_url': 'static/img/hero.jpg',
                    'category': 'Anime'
                }
            ]
            
            for item_data in sample_items:
                watchlist_item = WatchlistItem(
                    id=str(uuid.uuid4()),
                    user_id=sample_user.id,
                    title=item_data['title'],
                    image_url=item_data['image_url'],
                    category=item_data['category'],
                    created_at=datetime.utcnow()
                )
                db.session.add(watchlist_item)
            
            db.session.commit()
            
            print(f"✅ Created {len(sample_items)} sample watchlist items!")
            print("\nSample watchlist items:")
            for item in sample_items:
                print(f"  - {item['title']} ({item['category']})")
            
            return sample_user
            
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            db.session.rollback()
            return None

def test_database_operations():
    """Test basic database operations"""
    with app.app_context():
        try:
            print("\n🧪 Testing database operations...")
            
            # Test user query
            users = User.query.all()
            print(f"✅ Total users in database: {len(users)}")
            
            # Test watchlist query
            items = WatchlistItem.query.all()
            print(f"✅ Total watchlist items in database: {len(items)}")
            
            # Test filtering by category
            movies = WatchlistItem.query.filter_by(category='Movie').all()
            anime = WatchlistItem.query.filter_by(category='Anime').all()
            series = WatchlistItem.query.filter_by(category='Series').all()
            
            print(f"✅ Movies: {len(movies)}")
            print(f"✅ Anime: {len(anime)}")
            print(f"✅ Series: {len(series)}")
            
            # Test user-specific queries
            test_user = User.query.filter_by(username='testuser').first()
            if test_user:
                user_items = WatchlistItem.query.filter_by(user_id=test_user.id).all()
                print(f"✅ Test user's watchlist items: {len(user_items)}")
            
            print("✅ All database operations working correctly!")
            return True
            
        except Exception as e:
            print(f"❌ Database operation failed: {e}")
            return False

def main():
    """Main function to run the sample data creation and tests"""
    print("🚀 Creating sample data for Watchmate application...")
    print("=" * 50)
    
    # Create sample data
    user = create_sample_data()
    
    if user:
        print("\n" + "=" * 50)
        # Test database operations
        test_database_operations()
        
        print("\n" + "=" * 50)
        print("🎉 Sample data creation completed!")
        print("\nYou can now:")
        print("1. Start the application: python main.py")
        print("2. Go to http://localhost:5000")
        print("3. Login with:")
        print("   Username: testuser")
        print("   Password: password123")
        print("4. View the sample watchlist items in the dashboard")
    else:
        print("❌ Failed to create sample data")

if __name__ == '__main__':
    main()