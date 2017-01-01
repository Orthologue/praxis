# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# access the pyre framework
import pyre
# my protocol
from .Action import Action


# class declaration
class Command(pyre.panel(), implements=Action):
    """
    Base class for {praxis} commands
    """


# end of file
