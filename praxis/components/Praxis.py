# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access the pyre framework
import pyre
# my action protocol
from .Action import Action
# my protocols
from .. import compliance


# class declaration
class Praxis(pyre.plexus, family='praxis.components.plexus', action=Action):
    """
    The main {praxis} action dispatcher
    """


    # public state
    jurisdiction = compliance.jurisdiction(default='us.california')
    jurisdiction.doc = 'compliant calculators for the default company jurisdiction'


    # plexus obligations
    @pyre.export
    def help(self, **kwds):
        """
        Hook for the application help system
        """
        # get the package
        import praxis
        # show me
        self.info.log(praxis._praxis_usage)
        # all done
        return 0


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # build and attach my configuration options
        self.layout = self.newLayout()
        # all done
        return


    # implementation details
    layout = None


    # initialization hooks
    def newLayout(self):
        """
        Instantiate an object with the global project options
        """
        # pull in my layout
        from .Layout import Layout
        # and attach it
        return Layout()



# end of file 
