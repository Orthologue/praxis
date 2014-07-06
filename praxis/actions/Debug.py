# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# get the package
import praxis


# the action
class Debug(praxis.command, family='praxis.actions.debug'):
    """
    Development and debugging support
    """


    # command obligations
    @praxis.export
    def help(self, plexus, **kwds ):
        """
        Show a help screen
        """
        # show me
        self.info.log('debug support')
        self.info.line('usage: {.pyre_namespace} debug <aspect>'.format(plexus))
        self.info.log()
        # all done
        return 0


# end of file 
