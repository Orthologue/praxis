# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# declaration
class TypeRegistrar(dict):
    """
    Simplify schema access by building a map that enables id lookup for the typed data
    """


    # meta-methods
    def __init__(self, datastore, **kwds):
        # chain up
        super().__init__(**kwds)
        # index the category tables
        self.indexTypeTables(datastore=datastore)
        # all done
        return


    # implementation details
    def indexTypeTables(self, datastore):
        """
        Build an identity map from primary keys to themselves for each of the typed tables

        This map, though trivial, is useful in detecting inconsistencies during data priming,
        and providing the set of legal choices for type fields
        """
        # get the tables
        tables = datastore.schema.typeTables
        # go through each one
        for table in tables:
            # get the contents
            records = datastore.select(table)
            # build the index
            index = { eid: eid for eid, _ in datastore.select(table) }
            # and attach it
            self[table.pyre_name] = index
        # all done
        return


# end of file
