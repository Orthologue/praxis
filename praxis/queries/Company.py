# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# pull in the required  praxis parts
from .. import db, schema


# the query declaration
class Company(db.query, company=schema.company):
    """
    Retrieve a company record given its name
    """

    # the fields in the resulting records
    entity = company.entity
    name = company.name


    # meta-methods
    def __init__(self, entity=None, name=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # get my class so I can refer to my measures
        cls = type(self)

        # initialize the restriction
        where = cls.where

        # if i were handed a particular id
        if entity is not None:
            # here is the restriction i propose
            restriction = (cls.entity == entity)
            # add the restriction
            where = (where & restriction) if where is not None else restriction

        # if i were handed a particular name
        if name is not None:
            # here is the restriction i propose
            restriction = (cls.name == name)
            # add the restriction
            where = (where & restriction) if where is not None else restriction

        # save the restriction
        self.where = where

        # all done
        return


# end of file
