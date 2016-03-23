# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis
# access to the table of people
from .Person import Person


# table declaration
class Employee(praxis.db.table, id='employees'):
    """
    Personal information about employees
    """

    employee = praxis.db.reference(key=Person.entity).primary()
    employee.doc = "the entity whose attributes these are"

    # tax id
    tin = praxis.db.str().notNull()
    tin.doc = "the employee's tax id"

    identification = praxis.db.str(default=praxis.db.null)
    identification.doc = "government issued id number"

    birthday = praxis.db.date(default=praxis.db.null)
    birthday.doc = "the employee's date of birth"


# end of file
