# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# pull in the requirements
from .. import db, schema


# the query declaration
class EmployeeListing(db.query,
                      person = schema.crm.person,
                      employee = schema.hr.employee,
                      company = schema.crm.company,
                      employment = schema.hr.employment):
    """
    Retrieve active employees that work for a given company
    """


    # the fields in the resulting records
    eid = employment.id
    first = person.first
    last = person.last
    ssn = employee.tin
    effective = employment.effective
    until = employment.until

    # the restriction
    where = (
        (person.entity == employee.employee) & # the person is an employee
        (person.entity == employment.employee) & # the employment info pertains to this person
        db.isNull(until) # the employee is active
    )

    # the collation
    order = db.cast(eid, db.int)


# end of file
