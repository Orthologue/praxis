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
    id.doc = "the employee id; meant to support external data sources"

    # the parties
    employee = praxis.db.reference(key=Entity.eid).notNull()
    employee.doc = "the employed entity"

    employer = praxis.db.reference(key=Entity.eid).notNull()
    employer.doc = "the employing entity"

    # payroll info
    rate = praxis.db.decimal(precision=9, scale=2)
    rate.doc = "the employee's pay rate for the duration of this employment"

    frequency = praxis.db.reference(key=PayFrequency.id).notNull()
    frequency.doc = "the frequency with which pay check are issued; e.g.: biweekly"

    type = praxis.db.reference(key=PayType.id).notNull()
    type.doc = "the pay type; e.g. hourly or salary"


# end of file 
