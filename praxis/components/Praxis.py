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


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # pull in my layout
        from .Layout import Layout
        # and attach it
        self.layout = Layout()

        # all done
        return


    # implementation details
    layout = None


# end of file 
