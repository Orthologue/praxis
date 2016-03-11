# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# pull in the required  praxis parts
from .. import db, schema


# the query declaration
class Employee(db.query,
                 person=schema.person,
                 employee=schema.employee,
                 company=schema.company,
                 employment=schema.employment,
                 ):
    """
    Retrieve an employee record given an employment id
    """

    # the fields in the resulting records
    eid = employment.id
    first = person.first
    last = person.last


    # meta-methods
    def __init__(self, eid=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # if necessary
        if eid is not None:
            # here is my class
            cls = type(self)
            # and the restriction i propose
            restriction = (cls.eid == eid)
            # add the restriction
            self.where = cls.where & restriction if cls.where is not None else restriction
        # all done
        return


# end of file
