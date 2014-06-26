# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import os
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

    # constants
    pyre_namespace = 'praxis'

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


    def pyre_mountApplicationFolders(self):
        # chain up
        pfs = super().pyre_mountApplicationFolders()

        # get my installation folder
        prefix = self.prefix
        # and my name
        name = self.pyre_namespace
        # look for my data folder
        if prefix and self.pyre_namespace:
            # the name of my data folder
            alias = 'etc'
            # it should be at {prefix}/{alias}/{name}; e.g. {~/tools/etc/praxis}
            physical = os.path.join(prefix, alias, name)
            # if this exists
            if os.path.isdir(physical):
                # mount it as {name}/{alias}; e.g. {/praxis/etc}
                logical = self.vfs.local(root=physical).discover()
                # and attach it to my private filespace
                pfs[alias] = logical

        # and return the {pfs}
        return pfs


# end of file 
