#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

"""
Create the database
"""

def create():
    # access the package
    import pyre.db
    # build a database component
    db = pyre.db.postgres()
    # verify it is going to attach to the default database that is guaranteed to exist
    assert db.database == "postgres"
    # attach
    db.attach()
    # create the pyre database
    db.createDatabase(name="praxis")
    # and return the component
    return db

# main
if __name__ == "__main__":
    create()

# end of file 
