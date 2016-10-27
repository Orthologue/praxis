# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# super class
from .Tender import Tender


# declaration
class CreditCard(Tender):
    """
    A credit card payment
    """


    # constants
    mode = 'credit'


# end of file
