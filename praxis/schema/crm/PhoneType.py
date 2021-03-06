# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# access to my superclass
from .. import base


# table declaration
class PhoneType(base.type, id='phone_types'):
    """
    A table of the various types of phone numbers

    The current primer fills this table with the following values:
        cell, voice, fax, pager
    """


# end of file
