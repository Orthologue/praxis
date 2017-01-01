# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# super class
from .Tender import Tender


# declaration
class DebitCard(Tender):
    """
    A debit card payment
    """


    # constants
    mode = 'debit'


# end of file
