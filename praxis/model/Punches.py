# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import itertools, operator


# declaration
class Punches(list):
    """
    Encapsulation of the time spent on specific tasks during a work period
    """


    # types
    from .Task import Task as task


    # public data
    @property
    def hours(self):
        """
        Compute the total number of hours worked during this work period
        """
        # compute the total number of hours in this work period
        return sum(task.hours for task in self.billable)


    @property
    def breaks(self):
        """
        Compute the total amount of time in this work period that was not covered by the recorded
        tasks
        """
        # double up on the billables
        this, after = itertools.tee(self.billable)
        # make sure after starts at the second billable task, if it exists
        next(after, None)
        # sum up the time in between tasks
        return sum((t2.start - t1.finish).total_seconds()/3600 for t1,t2 in zip(this, after))


    @property
    def billable(self):
        """
        The sequence of my billable tasks
        """
        # just skip the non-billable tasks
        yield from (task for task in self if task.billable)
        # all done
        return


    # interface
    def newTask(self, name, start, finish):
        """
        Create and store a new task in this work period
        """
        # build one
        task = self.task(name=name, start=start, finish=finish)
        # store it
        self.append(task)
        # sort me
        self.sort(key=operator.attrgetter('start'))
        # and return it
        return task


# end of file
