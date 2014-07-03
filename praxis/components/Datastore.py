# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import pyre


# declaration
class Datastore(pyre.db.client, family="praxis.datastore"):
    """
    The base class for {praxis} components that connect to the database
    """


    # convenience
    from .. import schema, queries, support


    # interface
    def select(self, query):
        """
        Run query against my data store and return the results
        """
        # easy enough
        return self.server.select(query=query)


    def sqlRenderer(self):
        """
        Grant access to the SQL renderer
        """
        # easy enough
        return self.server.sql


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # establish the connection
        self.server.attach()
        # all done
        return


# end of file 
