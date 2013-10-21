# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# access to the framework
import praxis
# my superclass
from .Temporary import Temporary
# and the tables i refer to
from .Entity import Entity


# table declaration
class Employment(Temporary, id='employments'):
    """
    Establishing an employee-employer relationship between two entities
    """

    id = praxis.db.str().primary()
    employee = praxis.db.reference(key=Entity.eid).notNull()
    employer = praxis.db.reference(key=Entity.eid).notNull()


# end of file 
