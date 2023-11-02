# p2app/engine/main.py
#
# ICS 33 Fall 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

from p2app.events import *
from .database import Database

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self._database = None
        pass


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        try :
            if isinstance(event, QuitInitiatedEvent):
                yield EndApplicationEvent()
            if isinstance(event, OpenDatabaseEvent):
                yield from self.open_database(event.path())
            if isinstance(event, CloseDatabaseEvent):
                self._database.close()
                yield DatabaseClosedEvent()
            if isinstance(event, StartContinentSearchEvent):
                yield from self.search_continent(event.continent_code(), event.name())
            if isinstance(event, LoadContinentEvent):
                continent = self._database.search_continent_by_id(event.continent_id())
                yield ContinentLoadedEvent(continent)
            if isinstance(event,SaveNewContinentEvent):
                yield from self.save_new_continent(event.continent())
            if isinstance(event, SaveContinentEvent):
                yield from self.save_continent(event.continent())
            if isinstance(event, StartCountrySearchEvent):
                yield from self.search_country(event.country_code(), event.name())
            if isinstance(event, LoadCountryEvent):
                country = self._database.search_country_by_id(event.country_id())
                yield CountryLoadedEvent(country)
            if isinstance(event, SaveNewCountryEvent):
                yield from self.save_new_country(event.country())
            if isinstance(event, SaveCountryEvent):
                yield from self.save_country(event.country())
            if isinstance(event, StartRegionSearchEvent):
                yield from self.search_region(event.region_code(), event.local_code(), event.name())
            if isinstance(event, LoadRegionEvent):
                region = self._database.search_region_by_id(event.region_id())
                yield RegionLoadedEvent(region)
            if isinstance(event, SaveNewRegionEvent):
                yield from self.save_new_region(event.region())
            if isinstance(event, SaveRegionEvent):
                yield from self.save_region(event.region())
        except Exception as e :
            yield ErrorEvent(e.__str__())


    def open_database(self, path):
        """ A generator function that opens the database and generates
         events based on the success of opening the database"""
        self._database = Database(path)
        self._database.open()
        if self._database.check_database_correctness():
            yield DatabaseOpenedEvent(path)
        else:
            yield DatabaseOpenFailedEvent("Wrong file was opened. Please try again")


    def search_continent(self, continent_code, name):
        """ Generator function that searches for continents in database
         and generates events based on the search"""
        searched_continents = self._database.search_continent(continent_code, name)
        if searched_continents is not None:
            for continent in searched_continents:
                yield ContinentSearchResultEvent(continent)


    def save_new_continent(self, continent: Continent):
        """ Generator function that saves a new continent in the database
         and generates events based on the success or failure of the process"""
        continent_id, continent_code, name = continent
        error = self._database.save_new_continent(continent)
        if error is None:
            continent = next(self._database.search_continent(continent_code, name))
            yield ContinentSavedEvent(continent)
        else:
            yield SaveContinentFailedEvent("Save New Continent Failed.\n" + error)


    def save_continent(self, continent: Continent):
        """ Generator function that updates an existing continent in the database
         and generates events based on the success or failure of the process"""
        error = self._database.update_continent(continent)
        if error is None:
            yield ContinentSavedEvent(continent)
        else:
            yield SaveContinentFailedEvent("Save Continent Failed.\n" + error)


    def search_country(self,country_code, name):
        """ Generator function that searches for countries in database
         and generates events based on the search"""
        searched_countries = self._database.search_country(country_code, name)
        if searched_countries is not None:
            for country in searched_countries:
                yield CountrySearchResultEvent(country)


    def save_new_country(self, country: Country):
        """ Generator function that saves a new country in the database
         and generates events based on the success or failure of the process"""
        error = self._database.save_new_country(country)
        if error is None:
            created_country = next(self._database.search_country(country.country_code, country.name))
            yield CountrySavedEvent(created_country)
        else:
            yield SaveCountryFailedEvent("Save New Country Failed.\n" + error)


    def save_country(self, country: Country):
        """ Generator function that updates an existing country in the database
        and generates events based on the success or failure of the process"""
        error = self._database.update_country(country)
        if error is None:
            yield CountrySavedEvent(country)
        else:
            yield SaveCountryFailedEvent("Save Continent Failed.\n" + error)


    def search_region(self, region_code, local_code, name):
        """ Generator function that searches for regions in database
         and generates events based on the search"""
        searched_regions = self._database.search_region(region_code, local_code, name)
        if searched_regions is not None:
            for region in searched_regions:
                yield RegionSearchResultEvent(region)


    def save_new_region(self, region:Region):
        """ Generator function that saves a new region in the database
        and generates events based on the success or failure of the process"""
        error = self._database.save_new_region(region)
        if error is None:
            created_region = next(self._database.search_region(region.region_code, region.local_code, region.name))
            yield RegionSavedEvent(created_region)
        else:
            yield SaveRegionFailedEvent("Save New Region Failed.\n" + error)


    def save_region(self, region:Region):
        """ Generator function that updates an existing region in the database
            and generates events based on the success or failure of the process"""
        error = self._database.update_region(region)
        if error is None:
            yield RegionSavedEvent(region)
        else:
            yield SaveRegionFailedEvent("Save Region Failed.\n" + error)