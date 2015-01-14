# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# declaration
class Builder:


    # interface
    def createTables(self, datastore, tables=None):
        """
        Create the table structure of my database
        """
        # unpack the datastore connection
        server = datastore.server
        # and its schema
        schema = datastore.schema
        # if the caller didn't specify which tables to build, build them all
        tables = tables if tables is not None else {table.pyre_name for table in schema.tables}

        # go through the schema
        for table in schema.tables:
            # build all the requested tables
            if table.pyre_name in tables: server.createTable(table)

        # all done
        return self


    def dropTables(self, datastore, tables=None):
        """
        Remove all tables from the database; use with caution!
        """
        # unpack the datastore connection
        server = datastore.server
        # and its schema
        schema = datastore.schema
        # if the caller didn't specify which tables to build, build them all
        tables = tables if tables is not None else {table.pyre_name for table in schema.tables}

        # go through the schema
        for table in reversed(schema.tables):
            # build all the requested tables
            if table.pyre_name in tables: server.dropTable(table)

        # all done
        return self


# end of file
