# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import praxis
# my superclass
from .Temporary import Temporary
# and the tables i refer to
from .Entity import Entity
from .PayType import PayType
from .PayFrequency import PayFrequency


# table declaration
class Employment(Temporary, id='employments'):
    """
    Establishing an employee-employer relationship between two entities
    """

    id = praxis.db.str()
    employee = praxis.db.reference(key=Entity.eid).notNull()
    employer = praxis.db.reference(key=Entity.eid).notNull()
    rate = praxis.db.float()
    type = praxis.db.reference(key=PayType.id).notNull()
    frequency = praxis.db.reference(key=PayFrequency.id).notNull()


# end of file 
