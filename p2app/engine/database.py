import sqlite3
from p2app.events import Continent, Country, Region


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
        cursor = self._connection.execute(""" PRAGMA foreign_keys = ON; """)
        cursor.close()



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
        cursor.close()

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
        cursor.close()
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
        continent = cursor.fetchone()
        cursor.close()
        return Continent(*continent)


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
        cursor.close()
        self._connection.commit()


    def update_continent(self, continent: Continent):
        """Updates an existing continent in database with new continent code and name
        and returns error string if an error occurred."""
        if continent.continent_code.isspace() or  continent.continent_code == "":
            return "Continent Code can not be empty."
        if continent.name.isspace() or continent.name == "":
            return "Name can not be empty."
        try:
            cursor = self._connection.execute("""
                UPDATE continent
                SET continent_code = ? , name = ?
                WHERE continent_id = ?;
                """, (continent.continent_code, continent.name, continent.continent_id))
        except Exception as e:
            error = e.__str__()
            if "UNIQUE constraint" in error:
                return "Continent Code already exists."
            else:
                return error
        cursor.close()
        self._connection.commit()


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
        cursor.close()
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
        country = cursor.fetchone()
        cursor.close()
        return Country(*country)


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
        cursor.close()
        self._connection.commit()


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
        cursor.close()
        self._connection.commit()


    def search_region(self, region_code:str, local_code:str, name:str):
        """Searches database for regions and generates results as region named tuples"""
        if region_code is None and name is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM region
                WHERE local_code = ? ;
            """, (local_code,))
        elif region_code is None and local_code is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM region
                WHERE name = ? ;
            """, (name,))
        elif local_code is None and name is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM region
                WHERE region_code = ? ;
                """, (region_code,))
        elif local_code is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM region
                WHERE region_code = ? AND name = ? ;
                """, (region_code,name))
        elif region_code is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM region
                WHERE local_code = ? AND name = ? ;
                """, (local_code, name))
        elif name is None:
            cursor = self._connection.execute("""
                SELECT *
                FROM region
                WHERE region_code = ? AND local_code = ? ;
                """, (region_code, local_code))
        else:
            cursor = self._connection.execute("""
                SELECT *
                FROM region
                WHERE region_code = ? AND local_code = ? AND name = ? ;
            """, (region_code,local_code,name))

        regions = cursor.fetchall()
        cursor.close()
        if regions is not None:
            for region in regions:
                yield Region(*region)


    def search_region_by_id(self, region_id:int) -> Region:
        """Searches database for a region by its ID and returns it"""
        cursor = self._connection.execute("""
            SELECT *
            FROM region
            WHERE region_id = ? ;
            """, (region_id,) )
        region = cursor.fetchone()
        cursor.close()
        return Region(*region)


    def save_new_region(self, region:Region ):
        """Inserts a new region into the database and
         returns an error message if failed"""
        if region.region_code.isspace() or region.region_code == "":
            return "Region Code can not be empty."
        if region.local_code.isspace() or region.local_code == "":
            return "Local code can not be empty."
        if region.name.isspace() or region.name == "":
            return "Name can not be empty."
        if region.continent_id is None:
            return "Continent id can not be empty."
        if region.country_id is None:
            return "Country id can not be empty."
        try :
            cursor = self._connection.execute("""
                INSERT INTO region (region_code, local_code,
                 name, continent_id, country_id, wikipedia_link, keywords)
                VALUES (?,?,?,?,?,?,?)
            """, (region.region_code, region.local_code,
                 region.name, region.continent_id, region.country_id,
                 region.wikipedia_link, region.keywords))
        except Exception as e:
            error = e.__str__()
            if "UNIQUE constraint" in error:
                return "Region Code already exists."
            else:
                return error
        cursor.close()
        self._connection.commit()


    def update_region(self, region: Region):
        """Updates an existing region in the database with new values"""
        if region.region_code.isspace() or region.region_code == "":
            return "Region Code can not be empty."
        if region.local_code.isspace() or region.local_code == "":
            return "Local code can not be empty."
        if region.name.isspace() or region.name == "":
            return "Name can not be empty."
        if region.continent_id is None:
            return "Continent id can not be empty."
        if region.country_id is None:
            return "Country id can not be empty."
        try:
            cursor = self._connection.execute("""
                 UPDATE region 
                 SET region_code = ? , local_code = ?, name = ?, 
                 continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ?
                 WHERE region_id = ? ;
             """, (region.region_code, region.local_code,region.name, region.continent_id,
                   region.country_id, region.wikipedia_link, region.keywords, region.region_id))
        except Exception as e:
            error = e.__str__()
            if "UNIQUE constraint" in error:
                return "Region Code already exists."
            else:
                return error
        cursor.close()
        self._connection.commit()
