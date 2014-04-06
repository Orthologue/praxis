# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import praxis
# superclasses
from .DBClient import DBClient
from .Application import Application


# declaration
class DBApplication(DBClient, Application, family="praxis.shells.db"):
    """
    The base class for {praxis} applications that connect to the database
    """


    # user configurable state
    iddcfg = praxis.properties.uri(default='file:idd.cfg')
    iddcfg.doc = 'the configuration file with the persistent {idd} state'


    # meta methods
    def __init__(self, **kwds):
        # chain up to get things done
        super().__init__(**kwds)

        # notify the user that this app is starting up
        self.info.line("startup:".format(self))

        # let me know
        self.info.line("  connected to {.db.database!r}".format(self))

        # load the {idd} persistent state
        self.info.line("  reading idd persistent state from '{.iddcfg}'".format(self))
        self.pyre_executive.loadConfiguration(uri=self.iddcfg, locator=praxis.tracking.here())

        # make an idd
        self.info.line("  initializing idd ".format(self))
        self.idd = praxis.idd(name='praxis:idd')
        self.idd.save(uri=self.iddcfg)
        self.info.line("    first token: {0.idd.date}-{0.idd.tid}".format(self))

        # ready to go
        self.info.log()

        # all done
        return


    # private data
    idd = None


# end of file 
