# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# declaration
class Task:
    """
    Encapsulation of time worked on a task using pairs of timestamps to mark clock-in and
    clock-out. The format is

        (task name, clock-in timestamp, clock-out timestamp)
    """


    # public data
    name = None
    start = None
    finish = None
    billable = True


    @property
    def hours(self):
        """
        Compute the duration of this task in hours
        """
        # compute my duration and convert into hours
        return (self.finish - self.start).total_seconds() / 3600


    # meta-methods
    def __init__(self, name, start, finish, billable=billable, **kwds):
        # chain up
        super().__init__(**kwds)
        # record my info
        self.name = name
        self.start = start
        self.finish = finish
        self.billable = billable
        # all done
        return


# end of file
