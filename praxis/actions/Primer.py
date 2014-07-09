# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# get the package
import praxis


# the action
class Primer(praxis.command, family='praxis.actions.db'):
    """
    Direct access to the application database
    """


    # public state
    tables = praxis.properties.set(default=None, schema=praxis.properties.str())
    tables.doc = 'restrict the tables affected to this set'


    # command obligations
    @praxis.export
    def help(self, plexus, **kwds ):
        """
        Show a help screen
        """
        # here is the list of my commands
        commands = ' | '.join(['create', 'init', 'prime', 'clear', 'drop'])
        # show me
        self.info.log('provides direct access to my database')
        self.info.line('usage: {.pyre_namespace} db [{}]'.format(plexus, commands))
        self.info.log()
        # all done
        return 0


    # implementation details
    def create(self, plexus):
        """
        Create my database
        """
        # get the name of my database
        name = plexus.layout.project
        # tell me
        self.info.log('creating database {!r}'.format(name))

        # get the low level package
        import pyre.db
        # build a database component
        db = pyre.db.postgres()
        # verify it is going to attach to the default database that is guaranteed to exist
        assert db.database == "postgres"
        # attach
        db.attach()
        # create the pyre database
        db.createDatabase(name=name)

        # all done
        return 0


    def init(self, plexus):
        """
        Build a subset of the tables that capture my schema
        """
        # instantiate a connection to the datastore
        datastore = plexus.datastore
        # get the set of tables to build
        tables = self.tables
        # make a builder
        builder = plexus.builder
        # show me
        self.info.log('creating the schema: tables={}'.format(tables if tables else 'all'))
        # ask it to do the work
        builder.createTables(datastore=datastore, tables=tables)

        # all done
        return 0


    def prime(self, plexus):
        """
        Insert into the tables all the default/static data
        """
        # instantiate a connection to the datastore
        datastore = plexus.datastore
        # get the set of tables to build
        tables = self.tables
        # make a token generator
        idd = plexus.idd
        # make a primer
        primer = plexus.primer
        # get it to prime the static types
        self.info.log('priming static types')
        datastore.server.insert(*primer.primeTypes(plexus=plexus))
        # the basic client information
        self.info.log('priming company information')
        datastore.server.insert(*primer.primeCompanyInformation(plexus=plexus))
        # the initial staff records
        self.info.log('priming staff records')
        datastore.server.insert(*primer.primeStaffRecords(plexus=plexus))
        
        # save the token generator state
        idd.save()

        # all done
        return 0


    def clear(self, plexus):
        """
        Drop my tables
        """
        # instantiate a connection to the datastore
        datastore = plexus.datastore
        # get the set of tables to build
        tables = self.tables
        # make a builder
        builder = plexus.builder
        # show me
        self.info.log('clearing tables: {}'.format(tables if tables else 'all'))
        # ask it to do the work
        builder.dropTables(datastore=datastore, tables=tables)

        # all done
        return 0


    def drop(self, plexus):
        """
        Drop the entrire database
        """
        # get the name of my database
        name = plexus.layout.project
        # show me
        self.info.log('dropping database {!r}'.format(name))

        # access the low level package
        import pyre.db
        # build a database component
        db = pyre.db.postgres()
        # verify it is going to attach to the default database that is guaranteed to exist
        assert db.database == "postgres"
        # attach
        db.attach()
        # create the pyre database
        db.dropDatabase(name=name)

        # all done
        return 0


# end of file
