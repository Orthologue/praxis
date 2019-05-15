# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# access to the framework
import praxis
# access to my superclass
from .. import base
# and the tables i refer to
from .. import crm
from .EmploymentType import EmploymentType
from .PayType import PayType
from .PayFrequency import PayFrequency


# table declaration
class Employment(base.temporary, id='employments'):
    """
    Establish an employee-employer relationship between two entities
    """

    id = praxis.db.str()
    id.doc = "the employee id; meant to support external data sources"

    # the parties
    employee = praxis.db.reference(key=crm.entity.entity).notNull()
    employee.doc = "the employed entity"

    employer = praxis.db.reference(key=crm.entity.entity).notNull()
    employer.doc = "the employing entity"

    # payroll info
    type = praxis.db.reference(key=EmploymentType.type).notNull()
    type.doc = "the employment type; e.g. full time or part time"

    pay = praxis.db.reference(key=PayType.type).notNull()
    pay.doc = "the pay type; e.g. hourly or salary"

    rate = praxis.db.decimal(precision=9, scale=2)
    rate.doc = "the employee's pay rate for the duration of this employment"

    frequency = praxis.db.reference(key=PayFrequency.frequency).notNull()
    frequency.doc = "the frequency with which pay checks are issued; e.g.: biweekly"


# end of file
