# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# superclass
from .Type import Type


# table declaration
class PhoneType(Type, id='phone_types'):
    """
    A table of the various types of phone numbers

    The current primer fills this table with the following values:
        cell, voice, fax, pager
    """


# end of file
