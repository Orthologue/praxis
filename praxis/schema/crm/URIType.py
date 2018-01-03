# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# access to my superclass
from .. import base


# table declaration
class URIType(base.type, id='uri_types'):
    """
    A table of the various types of uris

    The current primer fills this table with the following values:
        web, facebook, instagram, twitter, vine, youtube
    """


# end of file
