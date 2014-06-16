# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# convenient access to the command base class
from .Command import Command as command


# the list of actions
def db():
    """
    Grant access to the raw database primer
    """
    # get the database primer
    from .Primer import Primer
    # and return it
    return Primer


# end of file
