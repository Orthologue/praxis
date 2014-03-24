#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

"""
Drop all database tables
"""

# access the package
import praxis

# app declaration
class Destroyer(praxis.dbapp, family='praxis.shells.tableDestructor'):
    """
    Drop the entire table set
    """

    # configurable state
    tables = praxis.properties.set(default=None, schema=praxis.properties.str())

    # application obligations
    @praxis.export
    def main(self, *args, **kwds):
        """
        Drop all database tables
        """
        # make sure we are dropping tables from the {praxis} database
        assert self.db.database == 'praxis'
        # get my builder to do it
        self.builder.dropTables(db=self.db, schema=self.schema, tables=self.tables)
        # and report success
        return 0

# main
if __name__ == "__main__":
    # build the app
    app = Destroyer(name='praxis:destroyer')
    # and run it
    status = app.run()
    # send the result to the shell
    import sys
    sys.exit(status)

# end of file 
