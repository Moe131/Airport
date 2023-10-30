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


    def search_continent(self , continent_code: int, name: str) -> Continent:
        """Searches database for continents and generates results as Continent named tuples"""
        cursor = self._connection.execute("""
            SELECT continent_id, continent_code, name 
            FROM continent
            WHERE continent_code = ? AND name = ? ;
            """,(continent_code, name) )
        continent = cursor.fetchone()
        if continent is not None:
            return Continent(*continent)


    def search_continent_by_id(self, continent_id:int) -> Continent:
        """Searches database for a continent by its ID and returns it"""
        cursor = self._connection.execute("""
            SELECT continent_id, continent_code, name 
            FROM continent
            WHERE continent_id = ? ;
            """, (continent_id,) )
        return Continent(*cursor.fetchone())


    def save_new_continent(self, continent:Continent) -> None:
        """Inserts a new continent into the database"""
        continent_id, continent_code, name = continent
        cursor = self._connection.execute("""
            INSERT INTO continent (continent_code, name)
            VALUES (?,?); 
            """, (continent_code, name))


