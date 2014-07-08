# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import praxis


# table declaration
class Employee(praxis.db.table, id='employees'):
    """
    Personal information about employees
    """

    employee = praxis.db.reference(key=Entity.eid).notNull()

    tin = praxis.db.str().notNull()
    idn = praxis.db.str(default=praxis.db.null)
    dob = praxis.db.date().notNull()


# end of file 
