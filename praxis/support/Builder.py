# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# access to the framework
from .. import schema


# declaration
class Builder:


    # public data
    datastore = None


    # interface
    def createTables(self, tables):
        """
        Create the table structure of my database
        """
        # cache
        db = self.datastore

        # if the caller didn't specify which tables to build
        if not tables:
            # build them all
            tables = {table.pyre_name for table in schema.tables}

        # go through the schema
        for table in schema.tables:
            # build all the requested tables
            if table.pyre_name in tables: db.createTable(table)

        # all done
        return self


    def dropTables(self, tables):
        """
        Remove all tables from the database; use with caution!
        """
        # cache
        db = self.datastore

        # if the caller didn't specify which tables to build
        if not tables:
            # build them all
            tables = {table.pyre_name for table in schema.tables}

        # go through the schema
        for table in reversed(schema.tables):
            # build all the requested tables
            if table.pyre_name in tables: db.dropTable(table)

        # all done
        return self


    # meta-methods
    def __init__(self, datastore, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the datastore reference
        self.datastore = datastore
        # all done
        return


# end of file 
