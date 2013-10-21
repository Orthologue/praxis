#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

"""
Create all database tables
"""

# access the package
import praxis

# app declaration
class Creator(praxis.dbapp, family='praxis.shells.tableCreator'):
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
        # make sure we are creating tables in the {praxis} database
        assert self.db.database == 'praxis'
        # get my builder to do it
        self.builder.createTables(tables=self.tables)
        # and report success
        return 0

# main
if __name__ == "__main__":
    # build the app
    app = Creator(name='praxis:creator')
    # and run it
    status = app.run()
    # send the result to the shell
    import sys
    sys.exit(status)

# end of file 
