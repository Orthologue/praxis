# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# access to the framework
import praxis


# table declaration
class Temporary(praxis.db.table):
    """
    Mixin for tables with information that may become obsolete
    """

    # effective dates
    effective = praxis.db.date()
    until = praxis.db.date(default=praxis.db.null)


# end of file 
