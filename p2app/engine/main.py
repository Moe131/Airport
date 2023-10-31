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
            continent_code = event.continent_code()
            name = event.name()
            searched_continent = self._database.search_continent(continent_code,name)
            if searched_continent is not None:
                yield ContinentSearchResultEvent(searched_continent)

        if isinstance(event, LoadContinentEvent):
            continent_id = event.continent_id()
            continent = self._database.search_continent_by_id(continent_id)
            yield ContinentLoadedEvent(continent)

        if isinstance(event,SaveNewContinentEvent):
            continent_id, continent_code, name = event.continent()
            error = self._database.save_new_continent(event.continent())
            if error is None:
                continent = self._database.search_continent(continent_code, name)
                yield ContinentSavedEvent(continent)
            else:
                yield SaveContinentFailedEvent("Save New Continent Failed.\n" + error)