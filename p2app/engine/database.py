import sqlite3

class Database:
    """Represents the database of our application and allows us
    to connect, query, update and close the database"""

    def __init__(self, path):
        """Initializes the Database"""
        self._path = path
        self._connection = None

    def open(self) -> None:
        """Opens the database and starts a connection"""
        self._connection = sqlite3.connect(str(self._path))

    def close(self) -> None:
        """Closes the database connection"""
        self._connection.close()

    def check_open(self) -> bool :
        """Checks if the correct database is open and returns true if it is"""
        cursor = self._connection.execute('SELECT name FROM sqlite_schema;')
        if cursor.fetchone() == ('continent',) :
            return True
        else :
            return False


