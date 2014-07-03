# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# get the package
import praxis


# the action
class IDD(praxis.command, family='praxis.actions.idd'):
    """
    Direct access to the token generator
    """


    # public state
    token = praxis.properties.str(default=None)
    token.doc = 'an encoded token'

    counter = praxis.properties.str(default=None)
    counter.doc = 'use this counter to encode a token'

    date = praxis.properties.str(default=None)
    date.doc = 'use this date to encode a token'


    # command obligations
    @praxis.export
    def help(self, plexus, **kwds):
        """
        Show a help screen
        """
        # here is the list of my commands
        commands = ' | '.join(['decode', 'peek'])
        # show me
        self.info.log('direct access to the token generator')
        self.info.line('usage: {.pyre_namespace} idd [{}]'.format(plexus, commands))
        self.info.log()
        # all done
        return 0


    # action implementations
    def decode(self, plexus):
        """
        Decode the given {token} on the command line
        """
        # get the token
        token = self.token
        # check that we were given one
        if token is None:
            # and if not
            self.error.line('no token to decode')
            self.error.line('please supply a token')
            self.error.line('  using:')
            self.error.log('    {0.pyre_namespace} idd decode --token=<str>'.format(plexus))
            # indicate an error
            return 1


        # get the idd client
        idd = plexus.idd
        # normalize the token
        token = idd.normalize(token)
        # ask it to decode
        date, counter = idd.decode(token)

        # show me
        self.info.line('decoding token: {}'.format(token))
        self.info.line('    counter: {}'.format(counter))
        self.info.line('    date: {}'.format(date))
        self.info.line('    alphabet: {.alphabet}'.format(idd))
        self.info.log()

        # all done
        return


    def encode(self, plexus):
        """
        Decode the given {token} on the command line
        """
        # get my state
        date = self.date
        counter = self.counter

        # check that we were given enough information
        if counter is None or date is None:
            # and if not
            self.error.line('not enough information to encode a token')
            self.error.line('please supply a counter and a date')
            self.error.line('  using:')
            self.error.log(
                '    {0.pyre_namespace} idd encode --counter=<int> --date=<str>'.format(plexus))
            # indicate an error
            return 1

        # adjust for the presence of a four digit year
        if len(date) == 8:
            # by trimming from the top
            date = date[2:]

        # get the idd client
        idd = plexus.idd
        # ask it to decode the token
        token = idd.encode(tid=counter, date=date)
        # show me
        self.info.line('encoded token: {}'.format(token))
        self.info.line('    counter: {}'.format(counter))
        self.info.line('    date: {}'.format(date))
        self.info.line('    alphabet: {.alphabet}'.format(idd))
        self.info.log()

        # all done
        return


    def peek(self, plexus):
        """
        Show me the next token
        """
        # access the {idd} client
        idd = plexus.idd
        # show me
        self.info.line('peeking into the token generation sequence')
        # for now, interrogate the {idd} client state; this will not work when the client is
        # batching tokens received from a server, since the local client state may be in need
        # of a sync step with the server
        token = idd.encode(tid=idd.seed, date=idd.date)
        # show me
        self.info.line('next idd token: {}'.format(token))
        self.info.line('    seed: {.seed}'.format(idd))
        self.info.line('    date: {.date}'.format(idd))
        self.info.line('    alphabet: {.alphabet}'.format(idd))
        self.info.log()
        # all done
        return 0


# end of file