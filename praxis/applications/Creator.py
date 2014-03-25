# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

"""
Create all database tables
"""


# access the package
import praxis


# app declaration
class Creator(praxis.dbapp):
    """
    Build the entire table set
    """


    # configurable state
    tables = praxis.properties.set(default=None, schema=praxis.properties.str())


    # application obligations
    @praxis.export
    def main(self, *args, **kwds):
        """
        Build all database tables
        """
        # get my builder to do it
        self.builder.createTables(db=self.db, schema=self.schema, tables=self.tables)
        # and report success
        return 0


# end of file 
