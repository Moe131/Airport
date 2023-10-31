import sqlite3
from p2app.events import Continent, Country


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
                SELECT * 
                FROM continent
                WHERE name = ? ;
                """,(name,))
        elif name is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM continent
                WHERE continent_code = ? ;
                """,(continent_code,) )
        else:
            cursor = self._connection.execute("""
                SELECT *
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
            SELECT *
            FROM continent
            WHERE continent_id = ? ;
            """, (continent_id,) )
        return Continent(*cursor.fetchone())


    def save_new_continent(self, continent:Continent) :
        """Inserts a new continent into the database and
         returns the error message if failed"""
        if continent.continent_code.isspace() or  continent.continent_code == "":
            return "Continent Code can not be empty."
        if continent.name.isspace() or continent.name == "":
            return "Name can not be empty."
        try:
            cursor = self._connection.execute("""
                INSERT INTO continent (continent_code, name)
                VALUES (?,?); 
                """, (continent.continent_code, continent.name))
        except Exception as e:
            error = e.__str__()
            if "UNIQUE constraint" in error:
                return "Continent Code already exists."
            else :
                return error
        #self._connection.commit()


    def update_continent(self, continent_id:int, new_continent_code:int, new_name: str):
        """Updates an existing continent in database with new continent code and name
        and returns error string if an error occurred."""
        if new_continent_code.isspace() or  new_continent_code == "" or new_name.isspace() or new_name == "":
            return "Continent Code can not be empty."
        if new_name.isspace() or new_name == "":
            return "Name can not be empty."
        try:
            cursor = self._connection.execute("""
                UPDATE continent
                SET continent_code = ? , name = ?
                WHERE continent_id = ?;
                """, (new_continent_code, new_name, continent_id))
        except Exception as e:
            error = e.__str__()
            if "UNIQUE constraint" in error:
                return "Continent Code already exists."
            else:
                return error


    def search_country(self, country_code:int, name:str):
        """Searches database for countries and generates results as country named tuples"""
        if country_code is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM country
                WHERE name = ? ;
            """, (name,))
        elif name is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM country
                WHERE country_code = ? ;
            """, (country_code,))
        else:
            cursor = self._connection.execute("""
                SELECT *
                FROM country
                WHERE country_code = ? AND name = ? ;
            """, (country_code,name))

        countries = cursor.fetchall()
        if countries is not None:
            for country in countries:
                yield Country(*country)


    def search_country_by_id(self, country_id:int) -> Country:
        """Searches database for a country by its ID and returns it"""
        cursor = self._connection.execute("""
            SELECT *
            FROM country
            WHERE country_id = ? ;
            """, (country_id,) )
        return Country(*cursor.fetchone())

    def save_new_country(self, country:Country ):
        """Inserts a new country into the database and
         returns a error message if failed"""
        if country.country_code.isspace() or country.country_code == "":
            return "Country Code can not be empty."
        if country.name.isspace() or country.name == "":
            return "Name can not be empty."
        if country.wikipedia_link is None:
            return "Wikipedia link can not be empty."
        try :
            cursor = self._connection.execute("""
                INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords)
                VALUES (?,?,?,?,?)
            """, (country.country_code, country.name, country.continent_id, country.wikipedia_link, country.keywords))
        except Exception as e:
            error = e.__str__()
            if "UNIQUE constraint" in error:
                return "Country Code already exists."
            else:
                return error


    def update_country(self, country:Country):
        """Updates an existing country in the database with new values"""
        if country.country_code.isspace() or country.country_code == "":
            return "Country Code can not be empty."
        if country.name.isspace() or country.name == "":
            return "Name can not be empty."
        if country.wikipedia_link is None:
            return "Wikipedia link can not be empty."
        try:
            cursor = self._connection.execute("""
                UPDATE country 
                SET country_code = ?,  name = ? , continent_id = ?, wikipedia_link = ? , keywords = ?
                WHERE country_id = ? ;
            """, (country.country_code, country.name, country.continent_id,
              country.wikipedia_link, country.keywords, country.country_id) )
        except Exception as e:
            error = e.__str__()
            if "UNIQUE constraint" in error:
                return "Country Code already exists."
            else:
                return error
