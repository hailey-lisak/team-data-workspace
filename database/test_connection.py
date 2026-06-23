import psycopg2
import os

def test_db_connection_and_setup():
    connection = None
    try:
        print("🔄 Attempting to connect to local PostgreSQL...")
        
        # 1. Connect to your local Mac Postgres instance
        connection = psycopg2.connect(
            user="postgres",
            password="harper5802",  # <--- Replace this with your actual installer password!
            host="localhost",
            port="5432",
            database="postgres"  # Default database created by the installer
        )
        
        cursor = connection.cursor()
        
        # 2. Verify the connection by checking the database version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("✅ CONNECTION SUCCESSFUL!")
        print(f"   PostgreSQL Version: {db_version[0]}\n")
        
        # 3. Read and execute your create_tables.sql script
        sql_script_path = os.path.join(os.path.dirname(__file__), "create_tables.sql")
        
        print(f"📜 Reading database layout from {sql_script_path}...")
        with open(sql_script_path, "r") as sql_file:
            sql_script = sql_file.read()
            
        print("🛠️ Creating tables (users, workspaces, jobs, records)...")
        cursor.execute(sql_script)
        
        # Save the changes to the database
        connection.commit()
        print("🎉 SUCCESS: All tables built cleanly with no syntax errors!")
        
        cursor.close()
        
    except Exception as error:
        print(f"\n❌ SCRIPT FAILED: {error}\n")
        if connection:
            connection.rollback()
            
    finally:
        if connection:
            connection.close()
            print("\n🔒 Database connection closed cleanly.")

if __name__ == "__main__":
    test_db_connection_and_setup()