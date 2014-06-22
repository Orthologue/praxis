#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import pyre.parsing
import pyre.tracking
import pyre.patterns


# class declaration
class ScheduleParser(pyre.parsing.parser):
    """
    A simple parser for schedule specification files
    """


    # types
    from .ScheduleScanner import ScheduleScanner as lexer


    # interface
    def parse(self, uri, stream, locator):
        """
        Harvest the schedule events in {stream}
        """
        # initialize my context
        self.employee = []
        self.days = []
        # set up my processor
        processor = self.processor(locator)
        # tokenize the {stream}
        self.scanner.pyre_tokenize(uri=uri, stream=stream, client=processor)
        # all done
        return self.schedule


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the list of harvested tasks
        self.schedule = pyre.patterns.vivify(levels=2, atom=list)

        # the production table
        self.productions = {
            # the ignorables
            self.scanner.start: self.ignore,
            self.scanner.comment: self.ignore,
            self.scanner.whitespace: self.ignore,
            self.scanner.finish: self.ignore,
            # context specifier
            self.scanner.employee: self.processEmployee,
            }
        # and the list of errors encountered during parsing
        self.errors = []
        # all done
        return


    # implementation details
    @pyre.patterns.coroutine
    def processor(self, locator):
        """
        Receive tokens from the scanner and handle them
        """
        # for ever
        while True:
            # attempt to
            try:
                # get a token
                token = yield
            # if anything goes wrong
            except self.ParsingError as error:
                # save the error
                self.errors.append(error)
                # and move on
                continue

            # if we retrieved a well formed token, attempt to
            try:
                # look up the relevant production based on this terminal
                production = self.productions[type(token)]
            # if i don't have a production for this token
            except KeyError:
                # it must be a syntax error; build a locator
                loc = pyre.tracking.chain(this=token.locator, next=locator)
                # and an error
                error = self.SyntaxError(token=token, locator=loc)
                # save it
                self.errors.append(error)
                # move on
                continue
            # if all goes well, invoke the production
            yield from production(current=token)
        # all done
        return


    def ignore(self, **kwds):
        """
        Do nothing
        """
        # there is nothing to do here
        return []


    def processEmployee(self, current):
        """
        Process an {employee} token
        """
        # get the name of the employee
        employee = current.lexeme

        # while there are day specifications to process
        while True:
            # grab the next token
            days = yield
            # if it is not a day spec
            if type(days) is not self.scanner.days:
                # put it back
                self.scanner.pyre_pushback(days)
                # and bail
                return

            # convert the token into a list of days
            days = [ day.strip() for day in days.lexeme.split(',') ]

            # the current task is
            currentStation = None
            currentStart = None
            # now extract the assignments
            while True:
                # grab the next token
                task = yield
                # if it is a comment, ignore it
                if type(task) is self.scanner.comment: continue
                # if it is not a task
                if type(task) is not self.scanner.task:
                    # put it back
                    self.scanner.pyre_pushback(task)
                    # and bail
                    break
                # extract the station and the time
                station, time = tuple(item.strip() for item in task.lexeme.split('@'))
                # if i have a current task
                if currentStation:
                    # for every day it shows up
                    for day in days:
                        # it ends when this one starts
                        self.schedule[employee][day].append((currentStation, currentStart, time))
                # reset the current task
                currentStation = station
                # and its start time
                currentStart = time

        # all done
        return

# end of file 
