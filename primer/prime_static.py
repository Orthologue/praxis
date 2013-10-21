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
class Primer(praxis.dbapp, family='praxis.shells.primer'):
    """
    Place the static data in the database
    """

    # application obligations
    @praxis.export
    def main(self, *args, **kwds):
        """
        Prime all static data
        """
        # make sure we are creating tables in the {praxis} database
        assert self.db.database == 'praxis'

        # initialize the type tables
        self.initializeTypes()

        # store the state of {idd}
        self.idd.save(self.iddcfg)

        # and report success
        return 0


    # implementation details
    def initializeTypes(self):
        """
        Build the tables with type information
        """
        # get the token generator
        idd = self.idd
        # and the schema
        schema = self.schema
        # initialize the record pile
        records = []

        # aliases for the tables
        emails = schema.emailType
        # add them to the pile
        records += [
            # email types
            emails.pyre_immutable(id=idd(), description="home"),
            emails.pyre_immutable(id=idd(), description="work"),
            ]

        # store
        self.db.insert(*records)

        # all done
        return

# main
if __name__ == "__main__":
    # build the app
    app = Primer(name='praxis:primer')
    # and run it
    status = app.run()
    # send the result to the shell
    import sys
    sys.exit(status)


# end of file 
