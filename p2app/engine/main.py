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
        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.
        if isinstance(event, QuitInitiatedEvent):
            yield EndApplicationEvent()

        if isinstance(event, OpenDatabaseEvent):
            self._database = Database(event.path())
            self._database.open()
            if self._database.check_open():
                yield DatabaseOpenedEvent(event.path())
            else:
                yield DatabaseOpenFailedEvent("Wrong file was opened. Please try again")

        if isinstance(event, CloseDatabaseEvent):
            self._database.close()
            yield DatabaseClosedEvent()

        if isinstance(event, StartContinentSearchEvent):
            searched_continents = self._database.search_continent(event.continent_code(),event.name())
            if searched_continents is not None:
                for continent in searched_continents:
                    yield ContinentSearchResultEvent(continent)

        if isinstance(event, LoadContinentEvent):
            continent = self._database.search_continent_by_id(event.continent_id())
            yield ContinentLoadedEvent(continent)

        if isinstance(event,SaveNewContinentEvent):
            continent_id, continent_code, name = event.continent()
            error = self._database.save_new_continent(event.continent())
            if error is None:
                continent = next(self._database.search_continent(continent_code, name))
                yield ContinentSavedEvent(continent)
            else:
               yield SaveContinentFailedEvent("Save New Continent Failed.\n" + error)

        if isinstance(event, SaveContinentEvent):
            error = self._database.update_continent(event.continent())
            if error is None:
                yield ContinentSavedEvent(event.continent())
            else:
                yield SaveContinentFailedEvent("Save Continent Failed.\n" + error)

        if isinstance(event, StartCountrySearchEvent):
            searched_countries = self._database.search_country(event.country_code(),event.name())
            if searched_countries is not None:
                for country in searched_countries:
                    yield CountrySearchResultEvent(country)

        if isinstance(event, LoadCountryEvent):
            country = self._database.search_country_by_id(event.country_id())
            yield CountryLoadedEvent(country)

        if isinstance(event, SaveNewCountryEvent):
            country = event.country()
            error = self._database.save_new_country(country)
            if error is None:
                created_country = next(self._database.search_country(country.country_code, country.name))
                yield CountrySavedEvent(created_country)
            else:
                yield SaveCountryFailedEvent("Save New Country Failed.\n" + error)

        if isinstance(event, SaveCountryEvent):
            error = self._database.update_country(event.country())
            if error is None:
                yield CountrySavedEvent(event.country())
            else:
                yield SaveCountryFailedEvent("Save Continent Failed.\n"+ error)

        if isinstance(event, StartRegionSearchEvent):
            searched_regions = self._database.search_region(event.region_code(), event.local_code(), event.name())
            if searched_regions is not None:
                for region in searched_regions:
                    yield RegionSearchResultEvent(region)

        if isinstance(event, LoadRegionEvent):
            region = self._database.search_region_by_id(event.region_id())
            yield RegionLoadedEvent(region)

        if isinstance(event, SaveNewRegionEvent):
            region = event.region()
            error = self._database.save_new_region(region)
            if error is None:
                created_region = next(self._database.search_region(region.region_code, region.local_code,region.name))
                yield RegionSavedEvent(created_region)
            else:
                yield SaveRegionFailedEvent("Save New Region Failed.\n" + error)