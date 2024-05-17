import mysql.connector # pip install mysql-connector-python
from mysql.connector import Error


def create_schema_and_table(host, database, user, password):
    try:
        # Connect to the MySQL database server
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        if conn.is_connected():
            cursor = conn.cursor()

            # Create database if not exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS {};".format(database))
            conn.database = database

            # Create schema if not exists
            cursor.execute("CREATE SCHEMA IF NOT EXISTS ai385project;")

            # Create table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ai385project.usability_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    happy_prob VARCHAR(255),
                    sad_prob VARCHAR(255),
                    angry_prob VARCHAR(255),
                    neutral_prob VARCHAR(255),
                    path_similarity FLOAT,
                    task_usability VARCHAR(255)
                );
            """)
            print("Schema and table created successfully!")

        # Return the connection object
        return conn

    # Print any errors that occur during execution
    except Error as e:
        print(e)


def update_last_row(conn, happy_prob, sad_prob, angry_prob, neutral_prob, path_similarity, task_usability):
    try:
        cursor = conn.cursor()

        # Get the ID of the last row
        cursor.execute("SELECT id FROM ai385project.usability_results ORDER BY id DESC LIMIT 1;")
        last_row_id = cursor.fetchone()

        # Update the last row with the new data
        if last_row_id:
            cursor.execute("""
                UPDATE ai385project.usability_results
                SET happy_prob = %s, sad_prob = %s, angry_prob = %s, neutral_prob = %s, path_similarity = %s, task_usability = %s
                WHERE id = %s;
            """, (happy_prob, sad_prob, angry_prob, neutral_prob, path_similarity, task_usability, last_row_id[0]))
            conn.commit()

        else:
            print("No rows found to update.")

    # Print any errors that occur during execution
    except mysql.connector.Error as e:
        print(f"Error: {e}")


def insert_mouse_similarity(mouse_based_similarity):
    try:
        # Connect to the MySQL database server
        conn = mysql.connector.connect(
            host='localhost',
            database = 'ai385project',
            user='root',
            password='4010405'
        )

        # insert the mouse_based_similarity to the DB
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ai385project.usability_results 
            (path_similarity) 
            VALUES (%s);
        """, ( mouse_based_similarity,))
        conn.commit()

    # Print any errors that occur during execution
    except Error as e:
        print(e)


def fetch_path_similarity(conn):
    try:
        cursor = conn.cursor()
        # Formulate the query to fetch the last row's path_similarity
        cursor.execute(f"SELECT path_similarity FROM ai385project.usability_results ORDER BY id DESC LIMIT 1")

        # Fetch the result
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the path_similarity value
        else:
            return None  # Return None if no rows are found

    # Print any errors that occur during execution
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


