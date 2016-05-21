# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
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


    # action implementations
    @praxis.export(tip='decode a token from the command line')
    def decode(self, plexus, **kwds):
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
            self.error.log(
                '    {.pyre_namespace} {.pyre_spec} decode --token=<str>'.format(plexus, self))
            # indicate an error
            return 1


        # get the idd client
        idd = plexus.idd
        # normalize the token
        token = idd.normalize(token)
        # ask it to decode
        date, counter = idd.decode(token)

        # show me
        plexus.info.line('decoding token: {}'.format(token))
        plexus.info.line('    counter: {}'.format(counter))
        plexus.info.line('    date: {}'.format(date))
        plexus.info.line('    alphabet: {.alphabet}'.format(idd))
        plexus.info.log()

        # all done
        return


    @praxis.export(tip='encode a token from the command line')
    def encode(self, plexus, **kwds):
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
                '    {.pyre_namespace} {.pyre_spec} encode --counter=<int> --date=<str>'.format(
                    plexus, self))
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
        plexus.info.line('encoded token: {}'.format(token))
        plexus.info.line('    counter: {}'.format(counter))
        plexus.info.line('    date: {}'.format(date))
        plexus.info.line('    alphabet: {.alphabet}'.format(idd))
        plexus.info.log()

        # all done
        return


    @praxis.export(tip='show me the next token in the sequence with disturbing the generator')
    def peek(self, plexus, **kwds):
        """
        Show me the next token
        """
        # access the {idd} client
        idd = plexus.idd
        # show me
        plexus.info.line('peeking into the token generation sequence')
        # for now, interrogate the {idd} client state; this will not work when the client is
        # batching tokens received from a server, since the local client state may be in need
        # of a sync step with the server
        token = idd.encode(tid=idd.seed, date=idd.date)
        # show me
        plexus.info.line('next idd token: {}'.format(token))
        plexus.info.line('    seed: {.seed}'.format(idd))
        plexus.info.line('    date: {.date}'.format(idd))
        plexus.info.line('    alphabet: {.alphabet}'.format(idd))
        plexus.info.log()
        # all done
        return 0


# end of file
