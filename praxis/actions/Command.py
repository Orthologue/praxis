# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access the pyre framework
import pyre
# my protocol
from .. import components


# class declaration
class Command(pyre.panel, implements=components.action):
    """
    Base class for {praxis} commands
    """


# end of file
