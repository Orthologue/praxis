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

# main
if __name__ == "__main__":
    # build the app
    app = praxis.applications.destroyer(name='praxis:destroyer')
    # make sure we are dropping tables from the {praxis} database
    assert app.db.database == 'praxis'
    # and run it
    status = app.run()
    # send the result to the shell
    import sys
    sys.exit(status)

# end of file 
