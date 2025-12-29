"""
Migrate data from SQLite to Supabase PostgreSQL.

This script exports all data from the local SQLite database
and imports it into your Supabase PostgreSQL database.

WARNING: This will ADD data to Supabase. If tables have data, you may get conflicts.
         Run init_supabase_db.py first to create tables.

Usage:
    conda run -n blogsite python migrate_sqlite_to_supabase.py
"""
import os
import sys
import sqlite3
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, MetaData

# Load environment variables
load_dotenv()

# Paths
SQLITE_DB = 'database.sqlite3'
POSTGRESQL_URL = os.environ.get('DATABASE_URL')

def migrate_data():
    """Export data from SQLite and import to Supabase."""
    
    print("=" * 60)
    print("SQLite to Supabase Migration")
    print("=" * 60)
    
    # Check prerequisites
    if not POSTGRESQL_URL:
        print("\n❌ ERROR: DATABASE_URL not set in .env file!")
        sys.exit(1)
    
    if not os.path.exists(SQLITE_DB):
        print(f"\n❌ ERROR: SQLite database not found: {SQLITE_DB}")
        print("No data to migrate.")
        sys.exit(1)
    
    # Connect to SQLite
    print(f"\n📂 Opening SQLite database: {SQLITE_DB}")
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_conn.row_factory = sqlite3.Row
    
    # Connect to PostgreSQL
    print(f"🔌 Connecting to Supabase PostgreSQL...")
    pg_engine = create_engine(POSTGRESQL_URL)
    
    # Define migration order (respects foreign keys)
    tables = ['user', 'post', 'following', 'like', 'comment']
    
    total_migrated = 0
    
    try:
        with pg_engine.connect() as pg_conn:
            print("\n🚀 Starting migration...")
            print("-" * 60)
            
            for table in tables:
                print(f"\n📊 Migrating table: {table}")
                
                # Get data from SQLite
                cursor = sqlite_conn.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                if not rows:
                    print(f"   ⚠️  No data in {table} - skipping")
                    continue
                
                # Insert into PostgreSQL
                migrated = 0
                errors = 0
                
                for row in rows:
                    try:
                        # Build INSERT statement with quoted table names for PostgreSQL
                        columns = ', '.join([f'"{k}"' for k in row.keys()])
                        placeholders = ', '.join([f":{k}" for k in row.keys()])
                        # Quote table name if it's a reserved keyword
                        table_quoted = f'"{table}"' if table in ['user', 'like'] else table
                        sql = f"INSERT INTO {table_quoted} ({columns}) VALUES ({placeholders})"
                        
                        pg_conn.execute(text(sql), dict(row))
                        migrated += 1
                        
                    except Exception as e:
                        errors += 1
                        if errors == 1:  # Show first error only
                            print(f"   ⚠️  Error inserting row: {str(e)[:100]}")
                
                # Commit after each table
                pg_conn.commit()
                
                print(f"   ✅ Migrated {migrated} rows", end='')
                if errors > 0:
                    print(f" ({errors} errors - likely duplicates)")
                else:
                    print()
                
                total_migrated += migrated
            
            # Reset sequences for auto-increment columns
            print("\n🔄 Resetting auto-increment sequences...")
            for table in tables:
                cursor = sqlite_conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    # Find primary key column
                    pk_map = {
                        'user': 'id',
                        'post': 'post_id',
                        'like': 'like_id',
                        'following': 'follow_id',
                        'comment': 'comment_id'
                    }
                    pk_col = pk_map.get(table, 'id')
                    
                    # Get max ID
                    cursor.execute(f"SELECT MAX({pk_col}) FROM {table}")
                    max_id = cursor.fetchone()[0]
                    
                    if max_id:
                        # Reset PostgreSQL sequence
                        seq_name = f"{table}_{pk_col}_seq"
                        try:
                            pg_conn.execute(text(f"SELECT setval('{seq_name}', {max_id})"))
                            print(f"   ✅ Set {table} sequence to {max_id}")
                        except Exception as e:
                            print(f"   ⚠️  Could not set sequence for {table}: {str(e)[:50]}")
            
            pg_conn.commit()
            
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        sqlite_conn.close()
        sys.exit(1)
    
    sqlite_conn.close()
    
    print("\n" + "=" * 60)
    print(f"✅ Migration complete! Total rows migrated: {total_migrated}")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Verify data in Supabase dashboard → Table Editor")
    print("2. Test login with an existing user")
    print("3. Start application: conda run -n blogsite python main.py")
    print("\n⚠️  Keep your SQLite backup: database.sqlite3.backup")

if __name__ == '__main__':
    # Confirm before migrating
    print("\n⚠️  WARNING: This will copy data from SQLite to Supabase")
    print("Make sure you have:")
    print("  1. Created Supabase project")
    print("  2. Run init_supabase_db.py to create tables")
    print("  3. Backed up your SQLite database")
    
    response = input("\nContinue? (yes/no): ").strip().lower()
    
    if response == 'yes':
        migrate_data()
    else:
        print("Migration cancelled.")
