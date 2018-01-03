# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# super class
from .Tender import Tender


# declaration
class Cash(Tender):
    """
    A cash payment
    """

    # constants
    mode = 'cash'


# end of file
