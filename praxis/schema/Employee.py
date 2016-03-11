# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis
# access to the table of entities
from .Entity import Entity


# table declaration
class Employee(praxis.db.table, id='employees'):
    """
    Personal information about employees
    """

    employee = praxis.db.reference(key=Entity.eid).notNull()
    employee.doc = "the entity whose attributes these are"

    # tax id
    tin = praxis.db.str().notNull()
    tin.doc = "the employee's tax id"

    idn = praxis.db.str(default=praxis.db.null)
    idn.doc = "government issued id number"

    dob = praxis.db.date(default=praxis.db.null)
    dob.doc = "the employee's birth date"


# end of file
