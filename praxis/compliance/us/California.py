# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# access the framework
import pyre
# externals
import datetime
import itertools
# and my protocol
from .. import jurisdiction


# class declaration
class California(pyre.component, implements=jurisdiction, family="praxis.compliance.us.california"):
    """
    Encapsulation of calculators compliant with California law
    """


    # public data
    # multipliers for the overtime tiers to be used to price out the labor
    # in California, there are three tiers
    overtimeTiers = (1.0, 1.5, 2.0)


    # interface
    @pyre.export
    def overtime(self, start, workweeks, timecard):
        """
        Classify the hours worked by an employee a given an employee's {timecard}. This calculator
        assumes that the work week starts on {start}, a {datetime.date} object, and will clip
        the calculation to {workweeks} consecutive work weeks.
        """
        # the counter increment
        day = datetime.timedelta(days=1)
        # go through the right number of work weeks
        for workweek in range(workweeks):
            # compute the dates in this work week
            days = tuple(start + (n + 7*workweek)*day for n in range(7))
            # compute the number of hours worked for each day in this work week
            hours = tuple(timecard[today].hours for today in days)
            # classify into the three tiers and return the stats for this work week
            yield self._overtime(hours=hours)

        # all done
        return


    @pyre.export
    def overtime2(self, start, workweeks, timecard):
        """
        Classify the hours worked by an employee a given an employee's {timecard}. This calculator
        assumes that the work week starts on {start}, a {datetime.date} object, and will clip
        the calculation to {workweeks} consecutive work weeks.
        """
        # units
        day = datetime.timedelta(days=1)
        # go through the requested number of work weeks
        for week in range(workweeks):
            # reset my regular hours counter
            reg = 0
            # reset the work days in this work week
            workdays = 0
            # go through the days in each work week
            for dow in range(7):
                # compute the date
                today = start + (week*7 + dow)*day
                # get the hours worked today
                worked = timecard[today].hours

                # if there were no work hours today
                if worked == 0:
                    # yield a null result
                    yield today, (0, 0, 0)
                    # and move on
                    continue

                # otherwise, increment the number of work days this week
                workdays += 1

                # classify:
                # every hour above 12 goes into double pay
                double = max(0, worked - 12)

                # get the number of hours below 12 but above 8
                excess = min(max(0, worked - 8), 4)
                # if this is the seventh consecutive workday this week
                if workdays == 7 :
                    # all overtime hours are double pay
                    double += excess
                    # and we have, as yet, no time-and-a-half
                    sesqui = 0
                # otherwise
                else:
                    # they are time-and-a-half
                    sesqui = excess

                # hours below 8 are candidates for regular pay
                unclassified = min(worked, 8)
                # the regular hours in any given work week are capped at 40
                available = 40 - reg
                # the regular hours are the smaller of these two
                regular = min(available, unclassified)
                # the rest are time-and-a-half
                sesqui += max(0, unclassified - available)

                # up the regular hour counter
                reg += regular

                # check the consistency to within a second
                assert (worked - regular - sesqui - double) < (1/3600)

                # yield the partial calculation
                yield today, (regular, sesqui, double)

        # all done
        return


    @pyre.export
    def breaks(self, start, workweeks, timecard) :
        """
        Same as {overtime} except the calculator enforces the legally mandated breaks
        """
        # in California, the work period is broken into blocks no longer than 6 hours separated
        # by 30 minute breaks

        # the counter increment
        day = datetime.timedelta(days=1)
        # go through the right number of work weeks
        for workweek in range(workweeks):
            # compute the dates in this work week
            days = tuple(start + (n + 7*workweek)*day for n in range(7))
            # adjust the hours
            hours = [ self.enforceBreaks(date=today, punches=timecard[today]) for today in days ]
            # classify into the three tiers and return the stats for this work week
            yield self._overtime(hours=hours)

        # all done
        return


    def enforceBreaks(self, date, punches):
        """
        Adjust the hours in the {punches} of a given shift to enforce the legally mandated breaks
        """
        # compute the hours worked
        worked = punches.hours
        # compute the breaks taken
        taken = punches.breaks
        # compute the mandated breaks
        mandated = .5 * int(worked/6)
        # compute the deficit
        deficit = mandated - taken
        # if the deficit is more than ten percent of what's required
        if deficit > .1 * mandated:
            # adjust the hours worked
            return worked - deficit
        # otherwise, return the actual value
        return worked


    # implementation details
    def _overtime(self, hours):
        """
        Classify the 7-tuple of {hours} worked in a given work week into the three pay tiers
        provided by California law
        """
        # compute the total hours worked in the week
        total = sum(hours)
        # figure out the number of working days
        workdays = len(tuple(filter(lambda x: x > 0, hours)))

        # counters
        double = 0
        sesqui = 0
        regular = 0

        # go though the hours
        for worked in hours:
            # every hour above 12 goes into double pay
            double += max(0, worked - 12)
            # every hour above 8 and below 12 goes into time and a half
            sesqui += min(max(0, worked - 8), 4)
            # all hours below 8 go into regular pay
            regular += min(worked, 8)

        # if the employee worked seven consecutive days in this work week, any overtime is
        # double pay
        if workdays == 7:
            # get the number of sesqui overtime hours worked on the seventh day
            seventh = min(max(0, hours[6] - 8), 4)
            # remove them from the sesqui tally and add them to double play
            sesqui -= seventh
            double += seventh

        # the weekly overtime tally is the number of hours in excess of 40 that are not
        # counted as double pay already
        weekly = max(total - double - 40, 0)
        # the employee is entitled to the largest of the two tallies
        sesqui = max(sesqui, weekly)
        # and the number of regular hours cannot exceed 40
        regular = min(regular, 40)

        # consistency check
        assert (total - regular - sesqui - double) < (1/3600) # expect second accuracy

        # all done
        return regular, sesqui, double


# end of file
