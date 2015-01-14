# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# get the package
import praxis


# the action
class Debug(praxis.command, family='praxis.actions.debug'):
    """
    Development and debugging support
    """

    # public state
    tables = praxis.properties.set(default=None, schema=praxis.properties.str())
    tables.doc = 'restrict the tables affected to this set'


    @praxis.export(tip='print the steps necessary to create the db schema')
    def dbinit(self, plexus):
        """
        Show me the statements necessary to create my schema
        """
        # the schema
        schema = plexus.schema
        # and the sql renderer
        sql = praxis.db.sql()

        # if the caller didn't specify which tables to build, build them all
        tables = self.tables or {table.pyre_name for table in schema.tables}

        # go through each table
        for table in schema.tables:
            # render
            for line in sql.createTable(table=table): print(line)

        # all done
        return 0


    @praxis.export(tip='debug the data model')
    def model(self, plexus):
        """
        Debug the model
        """
        # run the query
        companies = plexus.model.company.get(plexus=plexus, name=plexus.layout.company)
        # show me
        for company in companies: print(company)

        # all done
        return 0


# end of file
