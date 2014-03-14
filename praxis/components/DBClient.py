# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import pyre


# declaration
class DBClient(pyre.db.client, family="praxis.db.clients"):
    """
    The base class for {praxis} components that connect to the database
    """


    # convenience
    from .. import schema, queries


    # interface
    def lookup(self, query):
        """
        Run query against my data store and return the results
        """
        # easy enough
        return self.db.select(query=query)


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # establish the connection
        self.db.attach()

        # make a builder
        from ..support import builder
        self.builder = builder(datastore=self.db)

        # all done
        return


    # implementation details
    builder = None


# end of file 
