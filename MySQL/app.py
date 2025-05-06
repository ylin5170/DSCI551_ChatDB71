from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
from nl_to_sql import natural_language_to_sql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'movie_metadata'
}

def ensure_database_exists():
    """Create database and tables if they don't exist."""
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS movie_metadata")
        cursor.execute("USE movie_metadata")

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS title_basics (
                tconst VARCHAR(20) PRIMARY KEY,
                titleType VARCHAR(50),
                primaryTitle VARCHAR(255),
                originalTitle VARCHAR(255),
                isAdult BOOLEAN,
                startYear INT,
                endYear INT DEFAULT NULL,
                runtimeMinutes INT DEFAULT NULL,
                genres VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS title_ratings (
                tconst VARCHAR(20),
                averageRating FLOAT,
                numVotes INT,
                PRIMARY KEY (tconst),
                FOREIGN KEY (tconst) REFERENCES title_basics(tconst)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS title_principals (
                tconst VARCHAR(20),
                ordering INT,
                nconst VARCHAR(20),
                category VARCHAR(100),
                job VARCHAR(255),
                characters TEXT,
                PRIMARY KEY (tconst, ordering),
                FOREIGN KEY (tconst) REFERENCES title_basics(tconst)
            )
        """)

        cursor.close()
        conn.close()
        print("Database and tables checked/created.")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        exit(1)

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    nl_query = data.get("query", "")

    try:
        sql_query = natural_language_to_sql(nl_query)
        print("Generated SQL:\n", sql_query)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        results = []

        for stmt in sql_query.strip().split(";"):
            stmt = stmt.strip()
            if not stmt:
                continue

            try:
                cursor.execute(stmt)
                if stmt.lower().startswith(("select", "show")):
                    results = cursor.fetchall()
                else:
                    # Clear remaining results to avoid "Unread result found"
                    while cursor.nextset():
                        pass
            except mysql.connector.Error as err:
                print(f"⚠️ SQL Error for:\n{stmt}\n{err}")
                continue

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "sql": sql_query,
            "result": results
        })

    except Exception as e:
        print("Application Error:", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("Launching ChatDB Flask server...")
    ensure_database_exists()
    print("Starting Flask on http://127.0.0.1:5003")
    app.run(debug=True, port=5003)