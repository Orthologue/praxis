# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# superclass
from .Type import Type


# table declaration
class PayType(Type, id='pay_types'):
    """
    A table of the various compensation types

    The current primer fills this table with the following values:
        partner, contractor, hourly, salary
    """


# end of file
