# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# get the package
import praxis


# the action
class Staff(praxis.command, family='praxis.actions.staff'):
    """
    Direct access to the application database
    """


    # public state
    records = praxis.properties.istream(default=None)
    records.doc = 'the uri of the employee records'
    ecords = praxis.properties.str(default=None)


    # command obligations
    @praxis.export
    def help(self, plexus, **kwds):
        """
        Show a help screen
        """
        # here is the list of my commands
        commands = ' | '.join(['new', 'update', 'terminate'])
        # show me
        self.info.log('maintenance of employee records')
        self.info.line('usage: {.pyre_namespace} staff [{}]'.format(plexus, commands))
        self.info.log()
        # all done
        return 0


    # implementation details
    def new(self, plexus):
        """
        Select from the input stream the records that describe new employees only and add them to
        the database
        """
        # show me
        self.info.log('creating new employee records')

        # load the records
        for employee in self.readStaffRecords(plexus=plexus):
            # get the employee id
            eid = employee.id

        # all done
        return 0


    def update(self, plexus):
        """
        Build a subset of the tables that capture my schema
        """
        # show me
        self.info.log('updating employee records')

        # all done
        return 0


    def terminate(self, plexus):
        """
        Build a subset of the tables that capture my schema
        """
        # show me
        self.info.log('terminating an employee')

        # all done
        return 0


    # implementation details
    def readStaffRecords(self, plexus):
        """
        Read the staff records
        """
        # if i were not given the uri for the staff records
        if self.records is None:
            # attempt to build a reasonable default
            uri = self.URI_STAFF.format(plexus)
            print('setting the default value: uri={!r}'.format(uri))
            # attach it
            self.records = uri

        # attempt to
        try:
            # instantiate the record stream
            stream = self.records
        # and if that fails
        except self.FrameworkError as error:
            # show me
            self.error.line('missing file with employee records')
            self.error.line(error)
            self.error.line('please provide a uri for the employee records')
            self.error.line('  using:')
            self.error.log( '    {.pyre_namespace} staff new --records=<uri>'.format(plexus))
            # return with an error
            return 1
                            
        # otherwise, show me
        self.info.log('reading from {.records.name!r}'.format(self))
        # make a parser
        p = praxis.ingest.staff()
        # get the records
        yield from p.read(stream=stream, uri=stream.name)

        # all done
        return


    # constants
    URI_STAFF = 'vfs:/{0.pyre_namespace}/etc/staff.csv'
        

# end of file
