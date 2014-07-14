# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# the package
import praxis


# class declaration
class Company(praxis.db.object, schema=praxis.schema.company):
    """
    """


    @classmethod
    def get(cls, plexus, name='*'):
        """
        Retrieve all companies whose name matches the given regular expression
        """
        # build a query with the given regex
        q = cls.byName(name=name)
        # get the datastore
        datastore = plexus.datastore
        # run the query
        yield from datastore.select(q)


    # implementation details
    class byName(praxis.db.query, company=praxis.schema.company):
        """
        Retrieve companies by name
        """

        # my fields
        entity = company.entity
        name = company.name

        # meta-methods
        def __init__(self, name, **kwds):
            # chain up
            super().__init__(**kwds)
            # get my class record
            cls = type(self)
            # make a restriction and attach it
            self.where = praxis.db.like(field=cls.name, regex=name)
            # all done
            return

# end of file 
