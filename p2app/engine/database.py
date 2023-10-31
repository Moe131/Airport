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
        try:
            cursor = self._connection.execute('SELECT name FROM sqlite_schema;')
            if cursor.fetchone() == ('continent',) :
                return True
            else :
                return False
        except:
            return False




    def search_continent(self , continent_code: int, name: str) -> Continent:
        """Searches database for continents and generates results as Continent named tuples"""
        if continent_code is None :
            cursor = self._connection.execute("""
                SELECT continent_id, continent_code, name 
                FROM continent
                WHERE name = ? ;
                """,(name,))
        elif name is None:
            cursor = self._connection.execute("""
                SELECT continent_id, continent_code, name 
                FROM continent
                WHERE continent_code = ? ;
                """,(continent_code,) )
        else:
            cursor = self._connection.execute("""
                SELECT continent_id, continent_code, name 
                FROM continent
                WHERE continent_code = ? AND name = ? ;
                """,(continent_code, name) )

        continents = cursor.fetchall()
        if continents is not None:
            for continent in continents:
                yield Continent(*continent)


    def search_continent_by_id(self, continent_id:int) -> Continent:
        """Searches database for a continent by its ID and returns it"""
        cursor = self._connection.execute("""
            SELECT continent_id, continent_code, name 
            FROM continent
            WHERE continent_id = ? ;
            """, (continent_id,) )
        return Continent(*cursor.fetchone())


    def save_new_continent(self, continent:Continent) :
        """Inserts a new continent into the database and
         returns the error message if failed"""
        continent_id, continent_code, name = continent
        if continent_code.isspace() or  continent_code == "" or name.isspace() or name == "":
            return "Continent Code or Name can not be empty."
        try:
            cursor = self._connection.execute("""
                INSERT INTO continent (continent_code, name)
                VALUES (?,?); 
                """, (continent_code, name))
        except Exception as e:
            error = e.__str__()
            if "UNIQUE constraint" in error:
                return "Continent Code already exists."
            else :
                return error
        #self._connection.commit()

