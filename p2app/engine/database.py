import sqlite3
from p2app.events import Continent

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


    def search_continents(self , name: str, continent_code: int):
        """Searches database for continents and generates results as Continent named tuples"""
        cursor = self._connection.execute("""
        SELECT continent_id, continent_code, name 
        FROM continent
        WHERE continent_code = ? AND name = ? ;
        """,(continent_code, name) )

        yield Continent(*cursor.fetchone())






