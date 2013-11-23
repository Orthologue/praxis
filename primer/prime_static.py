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
        entities = schema.entityType
        locations = schema.locationType
        pay = schema.payType
        phones = schema.phoneType
        uris = schema.uriType

        # add them to the pile
        records += [
            # email types
            emails.pyre_immutable(id=idd(), description="home"),
            emails.pyre_immutable(id=idd(), description="work"),
            # entity types
            entities.pyre_immutable(id=idd(), description="companies"),
            entities.pyre_immutable(id=idd(), description="persons"),
            # location types
            locations.pyre_immutable(id=idd(), description="home"),
            locations.pyre_immutable(id=idd(), description="office"),
            locations.pyre_immutable(id=idd(), description="shipping"),
            locations.pyre_immutable(id=idd(), description="billing"),
            # pay types
            pay.pyre_immutable(id=idd(), description="hourly"),
            pay.pyre_immutable(id=idd(), description="salary"),
            # phone types
            phones.pyre_immutable(id=idd(), description="cell"),
            phones.pyre_immutable(id=idd(), description="fax"),
            phones.pyre_immutable(id=idd(), description="land line"),
            # uri types
            uri.pyre_immutable(id=idd(), description="web"),
            uri.pyre_immutable(id=idd(), description="facebook"),
            uri.pyre_immutable(id=idd(), description="instagram"),
            uri.pyre_immutable(id=idd(), description="twitter"),
            uri.pyre_immutable(id=idd(), description="vine"),
            uri.pyre_immutable(id=idd(), description="youtube"),
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
