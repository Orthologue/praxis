# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# declaration
class Punches(list):
    """
    Encapsulation of time worked using pairs of timestamps to mark clock-in and clock-out
    """


    # interface
    def hours(self):
        """
        Generate the number of hours worked based on the clock punches
        """
        # go through the punches
        for clockin, clockout in self:
            # compute the time difference
            delta = clockout - clockin
            # convert into a number of hours and yield it
            yield 24*delta.days + delta.seconds/3600

        # all done
        return


# end of file 