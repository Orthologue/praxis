# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# support
import praxis


# the action
class Transactions(praxis.command, family='praxis.actions.tj'):
    """
    Access to the ECRS transaction journal
    """


    # user configurable state
    log = praxis.properties.strings()
    log.doc = 'the list of log files to analyze'


    # behaviors
    @praxis.export(tip='parse and load transactions from journal logs')
    def load(self, plexus, **kwds):
        """
        Parse an ECRS transaction journal CSV report and extract the transaction information
        """
        # the fileserver
        vfs = plexus.vfs
        # get the journal channel
        info = plexus.info
        # get the uri fragments
        log = self.log

        # since this a potentially time consuming exercise, require the user to supply a
        # transaction log explicitly
        if not log:
            # complain
            plexus.error.log('please specify the transaction log to ingest')
            # and get some help
            return self.help(plexus=plexus)

        # if the user expressed an opinion, assemble the spec in a search pattern
        pattern = r'(?P<name>{})-tj.csv'.format('|'.join(log))
        # get the {cwd}
        cwd = vfs[vfs.STARTUP_DIR]

        # initialize the piles
        invoices = {} # actual customer transactions
        errors = [] # parsing errors
        warnings = [] # parsing warnings
        # make a parser
        parser = praxis.vendors.ecrs.reports.transactions()

        # sign in
        info.log('ingesting transactions:')
        info.log('    spec: {.log}'.format(self))
        # find the matches
        for node, match in cwd.find(pattern=pattern):
            # extract the file path
            name = match.group()
            # get the contents of the file
            with node.open() as stream:
                # show me
                info.log('  processing {}'.format(name))
                # pull in the data
                parser.parse(stream=stream, invoices=invoices, warnings=warnings, errors=errors)

        info.log('{:5} transactions'.format(len(invoices)))

        # all done
        return 0


# end of file
