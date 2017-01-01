# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# superclass
from .Type import Type


# table declaration
class URIType(Type, id='uri_types'):
    """
    A table of the various types of uris

    The current primer fills this table with the following values:
        web, facebook, instagram, twitter, vine, youtube
    """


# end of file
