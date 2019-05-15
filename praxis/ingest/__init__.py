# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# publish the local parsers
from .Mispunch import Mispunch as mispunch
from .Staff import Staff as staff


# helpers
def schedule(uri, stream, locator=None):
    """
    Extract a schedule from {stream}
    """
    # if i were not given a locator
    if locator is None:
        # get the tracking package
        import pyre.tracking
        # and make one
        locator = pyre.tracking.here(level=1)
    # get the parser factory
    from .ScheduleParser import ScheduleParser as parser
    # build a parser
    p = parser()
    # parse the stream
    schedule =  p.parse(uri=uri, stream=stream, locator=locator)
    # and return the schedule
    return schedule


# end of file
