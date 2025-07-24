#!/usr/bin/env python3
"""
Script to test Supabase connection and database setup
"""
import os
import sys
from sqlalchemy import text

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db

def test_connection():
    """Test the database connection"""
    with app.app_context():
        try:
            # Test basic connection
            result = db.session.execute(text('SELECT 1 as test'))
            print("✅ Database connection successful!")
            
            # Test if tables exist
            tables_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            
            result = db.session.execute(tables_query)
            tables = [row[0] for row in result]
            
            print(f"✅ Found {len(tables)} tables in database:")
            for table in tables:
                print(f"  - {table}")
            
            # Check if our required tables exist
            required_tables = ['users', 'watchlist']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"⚠️  Missing required tables: {missing_tables}")
                print("Run the migration files to create them.")
            else:
                print("✅ All required tables exist!")
            
            # Test table structure
            if 'users' in tables:
                users_structure = db.session.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'users'
                    ORDER BY ordinal_position;
                """))
                
                print("\n📋 Users table structure:")
                for row in users_structure:
                    nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                    print(f"  - {row[0]}: {row[1]} ({nullable})")
            
            if 'watchlist' in tables:
                watchlist_structure = db.session.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'watchlist'
                    ORDER BY ordinal_position;
                """))
                
                print("\n📋 Watchlist table structure:")
                for row in watchlist_structure:
                    nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                    print(f"  - {row[0]}: {row[1]} ({nullable})")
            
            # Test RLS policies
            if 'users' in tables and 'watchlist' in tables:
                rls_query = text("""
                    SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
                    FROM pg_policies
                    WHERE tablename IN ('users', 'watchlist')
                    ORDER BY tablename, policyname;
                """)
                
                policies = db.session.execute(rls_query)
                policy_list = list(policies)
                
                print(f"\n🔒 Found {len(policy_list)} RLS policies:")
                for policy in policy_list:
                    print(f"  - {policy[1]}.{policy[2]} ({policy[5]}) for {policy[4]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure you've connected to Supabase")
            print("2. Check that DATABASE_URL is set correctly")
            print("3. Verify your Supabase project is active")
            return False

def test_environment():
    """Test environment variables"""
    print("🔧 Checking environment variables...")
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Hide sensitive parts of the URL
        masked_url = database_url[:20] + "***" + database_url[-10:] if len(database_url) > 30 else "***"
        print(f"✅ DATABASE_URL is set: {masked_url}")
    else:
        print("❌ DATABASE_URL is not set")
        print("Please connect to Supabase first!")
        return False
    
    supabase_url = os.environ.get('SUPABASE_URL')
    if supabase_url:
        print(f"✅ SUPABASE_URL is set: {supabase_url}")
    else:
        print("⚠️  SUPABASE_URL is not set (optional)")
    
    return True

def main():
    """Main function"""
    print("🧪 Testing Supabase Connection for Watchmate")
    print("=" * 50)
    
    # Test environment
    if not test_environment():
        return
    
    print("\n" + "=" * 50)
    
    # Test connection
    if test_connection():
        print("\n🎉 Supabase connection test completed successfully!")
        print("\nNext steps:")
        print("1. Run: python create_sample_data.py")
        print("2. Start the app: python main.py")
    else:
        print("\n❌ Connection test failed!")

if __name__ == '__main__':
    main()