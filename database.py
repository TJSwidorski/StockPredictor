import sqlite3
import json

class StockTickerDatabase:
    @staticmethod
    def create_sets_table(connection):
        """
        Create the sets table in the database.

        :param connection: SQLite database connection
        """
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sets (
                id INTEGER PRIMARY KEY,
                set_name TEXT,
                set_data TEXT
            )
        """)
        connection.commit()

    @staticmethod
    def insert_set(connection, set_name, set_data):
        """
        Insert a set into the database.

        :param connection: SQLite database connection
        :param set_name: Name of the set
        :param set_data: Set data (list of strings)
        """
        serialized_data = json.dumps(set_data)  # Serialize the set to JSON string
        cursor = connection.cursor()
        cursor.execute("INSERT INTO sets (set_name, set_data) VALUES (?, ?)", (set_name, serialized_data))
        connection.commit()

    @staticmethod
    def retrieve_set(connection, set_name):
        """
        Retrieve a specific set from the database.

        :param connection: SQLite database connection
        :param set_name: Name of the set
        :return: Set data (list of strings)
        """
        cursor = connection.cursor()
        cursor.execute("SELECT set_data FROM sets WHERE set_name = ?", (set_name,))
        serialized_data = cursor.fetchone()[0]
        if serialized_data:
            return json.loads(serialized_data)  # Deserialize JSON string back to a list
        else:
            return None
        
    @staticmethod
    def retrieve_sets(connection):
        """
        Retrieve the names of all sets in the database.

        :param connection: SQLite database connection
        :return: List of set names
        """
        cursor = connection.cursor()
        cursor.execute("SELECT set_name FROM sets")
        set_names = [row[0] for row in cursor.fetchall()]
        return set_names