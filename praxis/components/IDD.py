# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import time
# access to the framework
import praxis


# declaration
class IDD(praxis.component, family="praxis.idd"):
    """
    The globally unique identifier generator
    """


    # user configurable state
    seed = praxis.properties.int()
    seed.doc = "the initial token seed"

    date = praxis.properties.str(default=None)
    date.doc = "the date to encode within the tokens"

    alphabet = praxis.properties.str(default="SVIXQK78WTUC93P6GJZBRHN2MAFED54LY")
    alphabet.doc = "the list of admissible characters"


    # public data
    cfg = 'file:idd.cfg'


    # factories
    @classmethod
    def create(cls, project, state):
        """
        Create an instance that is bound to the local configuration file
        """
        # load the configuration file
        cls.pyre_executive.loadConfiguration(state, locator=praxis.tracking.here())
        # build one
        idd = cls(name='{}_idd'.format(project), cfg=state)
        # ask it to save its state
        idd.save()
        # and return it
        return idd


    # interface
    def encode(self, tid, date):
        """
        Convert the given sequence number {tid} into a token within the given {date}
        """
        # combine the date and transaction id
        bcd = int(str(tid) + date)
        # generate a token and return it
        return "".join(reversed(tuple(self._encode(bcd))))


    def decode(self, token):
        """
        Convert a {token} back into a date and a sequence number
        """
        # initialize
        tid = 0
        base = self.base
        table = self.table
        # take the token apart
        for index, letter in enumerate(reversed(token.upper())):
            # decode by doing arithmetic in my base
            tid += table[letter] * base**index
        # render the transaction id into a string that is at least 7 letters long
        label = "{:07d}".format(tid)
        # extract the date and sequence number
        date = '20' + label[-6:]
        counter = int(label[:-6])
        # and return them
        return date, counter


    def reset(self):
        """
        Reset the token generation parameters
        """
        # get today's date
        today = time.strftime("%y%m%d", time.localtime())
        # if my date is old
        if not self.date or self.date < today:
            # adjust it
            self.date = today
            # and reset my sequence counter
            self.tid = 0
            # all done
            return
        # otherwise, leave my {date} alone; just set the sequence counter to my seed
        self.tid =  self.seed
        # all done
        return


    def save(self):
        """
        Save the current state in {uri}, assuming it is resolvable by the pyre fileserver
        """
        # grab the uri of my configuration file
        uri = self.cfg
        # ask the framework
        import pyre
        # for a weaver
        weaver = pyre.weaver.weaver(name='idd-weaver')
        # pick the language
        weaver.language = 'cfg'
        # open {uri}
        with self.pyre_fileserver.open(uri, mode='w') as stream:
            # get the weaver to do its thing
            for line in weaver.weave(document=self._renderState(renderer=weaver.language)):
                # store
                print(line, file=stream)
        # all done
        return


    def normalize(self, token):
        """
        Normalize the token so it is in canonical form
        """
        # currently, all tokens are upper case letters
        return token.upper()


    # meta-methods
    def __init__(self, cfg, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the uri of my configuration file
        self.cfg = cfg
        # set up my number base
        self.base = len(self.alphabet)
        # my hash table
        self.table = { letter: index for index,letter in enumerate(self.alphabet) }
        # reset my token generation parameters
        self.reset()
        # build my sequencer
        self.sequence = self._next()
        # all done
        return


    def __iter__(self):
        """
        Behave like an iterator
        """
        # i am one
        return self


    def __next__(self):
        """
        Get the next token in my sequence
        """
        # return the next token
        return next(self.sequence)


    def __call__(self):
        """
        When accessed as a callable
        """
        # return the next token
        return next(self.sequence)


    # implementation details
    def _next(self):
        """
        Make an iterator that generates tokens from my sequence
        """
        # forever
        while 1:
            # get my sequence number
            tid = self.tid
            # update the counter; must do it before yielding the token so that i can save my
            # state correctly in case i never get called again
            self.tid += 1
            # generate a token and return it
            yield self.encode(tid, self.date)

        # UNREACHABLE
        return


    def _encode(self, bcd):
        """
        Make a token
        """
        # initialize
        base = self.base
        alphabet = self.alphabet
        # go through the contents of {bcd}
        while 1:
            # split
            bcd, remainder = divmod(bcd, base)
            # hash and return a character
            yield alphabet[remainder]
            # check whether we are done
            if bcd == 0: break
        # all done
        return


    def _renderState(self, renderer):
        """
        Generate the sequence of lines necessary to represent my state
        """
        # place a marker
        yield renderer.commentLine('idd')
        # my name
        yield renderer.section(self.pyre_spec)
        # and each of my traits
        yield renderer.trait(name='seed', value=self.tid)
        yield renderer.trait(name='date', value=self.date)
        yield renderer.trait(name='alphabet', value=self.alphabet)
        # all done
        return


    # data
    base = 0
    table = None
    sequence = None


# end of file
