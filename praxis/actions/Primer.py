# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# get the package
import praxis


# the action
class Primer(praxis.command, family='praxis.actions.db'):
    """
    Direct access to the application database

    This family of commands build an initial snapshot of the datastore, including its schema,
    static data, and any initial information available in the filesystem
    """


    # public state
    tables = praxis.properties.set(default=None, schema=praxis.properties.str())
    tables.doc = 'restrict the tables affected to this set'

    sections = praxis.properties.set(
        schema = praxis.properties.str(),
        default = {'types', 'company', 'staff'})
    sections.doc = 'restrict the db sections to prime to this set'


    # basic commands
    @praxis.export(tip='create the database')
    def create(self, plexus):
        """
        Create my database
        """
        # get the name of my database
        name = plexus.layout.project
        # tell me
        plexus.info.log('creating database {!r}'.format(name))

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


    @praxis.export(tip='create database tables')
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
        plexus.info.log('creating the schema: tables={}'.format(tables if tables else 'all'))
        # ask it to do the work
        builder.createTables(datastore=datastore, tables=tables)

        # all done
        return 0


    @praxis.export(tip='fill the tables with initial data')
    def prime(self, plexus):
        """
        Insert into the tables all the default/static data
        """
        # make a primer
        primer = plexus.primer
        # get the sections
        sections = self.sections

        # if the static types section is on the pile
        if 'types' in sections:
            # get it to prime the static types
            plexus.info.log('priming static types')
            primer.primeTypes(plexus=plexus)

        # if the company info section is on the pile
        if 'company' in sections:
            # the basic client information
            plexus.info.log('priming company information')
            primer.primeCompanyInformation(plexus=plexus)

        # if the staff info section is on the pile
        if 'staff' in sections:
            # the initial staff records
            plexus.info.log('priming staff records')
            primer.primeStaffRecords(plexus=plexus)

        # save the token generator state
        plexus.idd.save()

        # all done
        return 0


    @praxis.export(tip='remove tables from the database')
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
        plexus.info.log('clearing tables: {}'.format(tables if tables else 'all'))
        # ask it to do the work
        builder.dropTables(datastore=datastore, tables=tables)

        # all done
        return 0


    @praxis.export(tip='remove the entire database')
    def drop(self, plexus):
        """
        Drop the entire database
        """
        # get the name of my database
        name = plexus.layout.project
        # show me
        plexus.info.log('dropping database {!r}'.format(name))

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


    # meta-commands
    @praxis.export(tip='recreate the database and its tables')
    def reset(self, plexus):
        """
        Revert the database to a known state
        """
        # clear, init, prime
        status = (
            self.clear(plexus=plexus) or
            self.init(plexus=plexus) or
            self.prime(plexus=plexus))
        # all done
        return status


# end of file
