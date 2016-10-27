# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# super class
from .Tender import Tender


# declaration
class ChargeAccount(Tender):
    """
    A payment with a house charge account
    """

    # constants
    mode = 'charge'


# end of file
