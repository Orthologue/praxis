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
    from .. import schema, queries, support


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

        # make a table builder
        self.builder = self.support.builder()
        # make a table primer
        self.primer =  self.support.primer()

        # all done
        return


    # implementation details
    builder = None
    primer = None


# end of file 
