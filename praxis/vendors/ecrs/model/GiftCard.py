# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# super class
from .Tender import Tender


# declaration
class GiftCard(Tender):
    """
    A payment with a store issued gift card
    """

    # public data
    account = None
    amount = 0


# end of file
