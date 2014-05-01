# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access the framework
import pyre
# externals
import datetime
# and my protocol
from .Jurisdiction import Jurisdiction as jurisdiction


# class declaration
class California(pyre.component,
                 implements = jurisdiction,
                 family = "praxis.compliance.california"):
    """
    Encapsulation of calculators compliant with California law
    """


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
            # the number of hours worked for each day in this work week
            hours = tuple(sum(timecard[current].hours()) for current in days)

            # classify into the three tiers and return the stats for this work week
            yield self._overtime(hours=hours)

        # all done
        return


    # public data 
    # multipliers for the three overtime tiers to be used to price out the labor; in California
    # there are three tiers
    overtimeTiers = (1.0, 1.5, 2.0)


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
