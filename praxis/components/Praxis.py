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
        # make my {idd} client
        self.idd = self.newIDD()
        # all done
        return


    # initialization hooks
    def pyre_loadLayout(self):
        """
        Instantiate an object with the global project options
        """
        # pull in my layout
        from .Layout import Layout
        # and attach it
        return Layout()


    def pyre_mountApplicationFolders(self, pfs, prefix):
        """
        Map the standard runtime folder layout into my private filespace

        Currently, there are two runtime folders that i am interested in:

           {prefix}/etc/{self.pyre_namespace}: contains application auxiliary data
           {prefix}/var/{self.pyre_namespace}: contains the application runtime state
        """
        # chain up
        pfs = super().pyre_mountApplicationFolders(pfs=pfs, prefix=prefix)

        # my runtime folders
        folders = [ 'etc', 'var' ]
        # go through them
        for folder in folders:
            # and mount each one
            self.pyre_mountPrivateFolder(pfs=pfs, prefix=prefix, folder=folder)

        # return my {pfs}
        return pfs


    # factories for support objects that can be overridden by subclasses
    def newBuilder(self):
        """
        Instantiate a table builder
        """
        # get the package
        from ..support import builder
        # instantiate and return it
        return builder()


    def newPrimer(self):
        """
        Instantiate a table primer
        """
        # get the package
        from ..support import primer
        # instantiate and return it
        return primer()


    def newIDD(self):
        """
        Instantiate a token generator client
        """
        # get the factory
        from . import idd
        # build one bound to the configuration file in my layout
        client = idd.create(project=self.layout.project, state=self.layout.iddcfg)
        # and return it
        return client


# end of file 
