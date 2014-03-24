# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# declaration
class Builder:


    # interface
    def createTables(self, db, schema, tables=None):
        """
        Create the table structure of my database
        """
        # if the caller didn't specify which tables to build, build them all
        tables = tables if tables is not None else {table.pyre_name for table in schema.tables}

        # go through the schema
        for table in schema.tables:
            # build all the requested tables
            if table.pyre_name in tables: db.createTable(table)

        # all done
        return self


    def dropTables(self, db, schema, tables=None):
        """
        Remove all tables from the database; use with caution!
        """
        # if the caller didn't specify which tables to build, build them all
        tables = tables if tables is not None else {table.pyre_name for table in schema.tables}

        # go through the schema
        for table in reversed(schema.tables):
            # build all the requested tables
            if table.pyre_name in tables: db.dropTable(table)

        # all done
        return self


# end of file 
