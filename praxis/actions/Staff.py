# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# get the package
import praxis


# the action
class Staff(praxis.command, family='praxis.actions.staff'):
    """
    A family of commands for maintaining employee information
    """


    # public state
    records = praxis.properties.istream(default=None)
    records.doc = 'the uri of the employee records'


    # implementation details
    @praxis.export(tip='process only records pertaining to new employees')
    def new(self, plexus, **kwds):
        """
        Select from the input stream the records that describe new employees only and add them to
        the database
        """
        # show me
        plexus.info.log('creating new employee records')

        # load the records
        for employee in self.readStaffRecords(plexus=plexus):
            # get the employee id
            eid = employee.id

        # all done
        return 0


    @praxis.export(tip='update the employee records')
    def update(self, plexus, **kwds):
        """
        Build a subset of the tables that capture my schema
        """
        # show me
        plexus.info.log('updating employee records')

        # all done
        return 0


    @praxis.export(tip='terminate an employee')
    def terminate(self, plexus, **kwds):
        """
        Build a subset of the tables that capture my schema
        """
        # show me
        plexus.info.log('terminating an employee')

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
            self.error.log( '    {.pyre_namespace} {.pyre_spec} new --records=<uri>'.format(
                plexus, self))
            # return with an error
            return 1

        # otherwise, show me
        plexus.info.log('reading from {.records.name!r}'.format(self))
        # make a parser
        p = praxis.ingest.staff()
        # get the records
        yield from p.read(stream=stream, uri=stream.name)

        # all done
        return


    # constants
    URI_STAFF = 'vfs:/{0.pyre_namespace}/etc/staff.csv'


# end of file
