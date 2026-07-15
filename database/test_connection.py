import psycopg2
import os
from dotenv import load_dotenv

# Load the keys from the .env file at the root of the project
#load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)


def test_db_connection_and_setup():
    connection = None
    try:
        print("🔄 Attempting to connect to local PostgreSQL securely...")
        
        # Fetch credentials securely from the environment variables
        db_host = os.getenv("DB_HOST", "db")        # <-- Defaults to 'db' (Docker network) instead of localhost!
        db_port = os.getenv("DB_PORT", "5432")
        db_user = os.getenv("DB_USER", "postgres")
        db_pass = os.getenv("DB_PASSWORD", "password123")
        db_name = os.getenv("DB_NAME", "postgres")

        print(f"📡 Connecting to {db_host}:{db_port} as user '{db_user}'...")

        connection = psycopg2.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name
        )
        
        #specific object responsible for taking a raw SQL command from Python, running it across the pipeline to the Postgres database, and bringing back the answer
        cursor = connection.cursor()
        
        # Verify connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("✅ SECURE CONNECTION SUCCESSFUL!")
        print(f"   PostgreSQL Version: {db_version[0]}\n")
        
        # Read and execute layout script
        sql_script_path = os.path.join(os.path.dirname(__file__), "create_tables.sql")
        print(f"📜 Reading database layout from {sql_script_path}...")
        # reads all text inside create_tables.sql file and turns it into a normal Python string variable
        with open(sql_script_path, "r") as sql_file:
            sql_script = sql_file.read()
            
        print("🛠️ Creating tables (users, workspaces, jobs, records)...")
        # hands massive string of SQL text to the runner and tells it to execute it in Postgres
        # tables are set up in temporary "draft" mode; they aren't permanently saved yet
        cursor.execute(sql_script)
        
        # permanently saves the tables once it runs perfectly with no syntax errors
        connection.commit()
        print("🎉 SUCCESS: All tables verified securely with no syntax errors!")
        cursor.close()
        
    except Exception as error:
        print(f"\n❌ SCRIPT FAILED: {error}\n")
        if connection:
            # deletes temporary tables built during this run so our db isn't corrupted if something breaks
            connection.rollback()
            
    finally:
        if connection:
            connection.close()
            print("\n🔒 Database connection closed cleanly.")

if __name__ == "__main__":
    test_db_connection_and_setup()