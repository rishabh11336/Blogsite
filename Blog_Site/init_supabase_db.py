"""
Initialize Supabase PostgreSQL database with schema.

This script creates all tables in your Supabase database
based on the SQLAlchemy models defined in model.py.

Usage:
    conda run -n blogsite python init_supabase_db.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if DATABASE_URL is set
if not os.environ.get('DATABASE_URL'):
    print("❌ ERROR: DATABASE_URL environment variable not set!")
    print("Please create a .env file with your Supabase connection string.")
    print("\nExample:")
    print("DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres")
    sys.exit(1)

# Import after loading env variables
from main import app, db
from model import User, Post, Like, Following, Comment

def init_database():
    """Create all tables in Supabase PostgreSQL database."""
    
    print("=" * 60)
    print("Supabase Database Initialization")
    print("=" * 60)
    
    # Show connection info (hide password)
    db_url = os.environ.get('DATABASE_URL', '')
    if '@' in db_url:
        parts = db_url.split('@')
        safe_url = parts[0].split(':postgresql://')[0] + "://postgres:***@" + parts[1]
    else:
        safe_url = "Not set"
    
    print(f"\n📊 Connecting to: {safe_url}")
    
    with app.app_context():
        try:
            # Test connection
            print("\n🔌 Testing database connection...")
            db.session.execute(db.text('SELECT 1'))
            print("✅ Connection successful!")
            
            # Create all tables
            print("\n🏗️  Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Verify tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📋 Created {len(tables)} tables:")
            for table in sorted(tables):
                columns = [col['name'] for col in inspector.get_columns(table)]
                print(f"   • {table}: {len(columns)} columns")
            
            # Verify indexes
            print(f"\n📑 Indexes created:")
            for table in sorted(tables):
                indexes = inspector.get_indexes(table)
                if indexes:
                    for idx in indexes:
                        print(f"   • {table}.{idx['name']}")
            
            print("\n" + "=" * 60)
            print("✅ Database initialization complete!")
            print("=" * 60)
            print("\nNext steps:")
            print("1. Start the application: conda run -n blogsite python main.py")
            print("2. Access at: http://localhost:8080")
            print("3. (Optional) Migrate data: conda run -n blogsite python migrate_sqlite_to_supabase.py")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            print("\nTroubleshooting:")
            print("1. Check your DATABASE_URL is correct")
            print("2. Verify Supabase project is running")
            print("3. Check your database password")
            print("4. Ensure psycopg2-binary is installed: conda run -n blogsite pip install psycopg2-binary")
            sys.exit(1)

if __name__ == '__main__':
    init_database()
