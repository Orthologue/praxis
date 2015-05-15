# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os
# access the pyre framework
import pyre
# my protocols
from .. import compliance


# class declaration
class Praxis(pyre.plexus, family='praxis.components.plexus'):
    """
    The main {praxis} action dispatcher
    """

    # constants
    pyre_namespace = 'praxis'
    # types
    from .Action import Action as pyre_action

    # public state
    jurisdiction = compliance.jurisdiction(default='us.california')
    jurisdiction.doc = 'compliant calculators for the default company jurisdiction'


    # public data
    from .. import schema, queries, model


    @property
    def builder(self):
        """
        Get my schema initializer
        """
        # if i don't have one already
        if self._builder is None:
            # build one
            self._builder = self.newBuilder()
        # return it
        return self._builder


    @property
    def datastore(self):
        """
        Get the connection to my data server
        """
        # if i don't have one already
        if self._datastore is None:
            # build one
            self._datastore = self.newDatastoreClient()
        # return it
        return self._datastore


    @property
    def idd(self):
        """
        Get the token generator client
        """
        # if i don't have one already
        if self._idd is None:
            # build one
            self._idd = self.newIDD()
        # return it
        return self._idd


    @property
    def primer(self):
        """
        Get the object that knows how to initialize the static data to the schema
        """
        # if i don't have one already
        if self._primer is None:
            # build one
            self._primer = self.newPrimer()
        # return it
        return self._primer


    @property
    def typeRegistrar(self):
        """
        Get the indexer of data categories
        """
        # if i don't have one already
        if self._typeRegistrar is None:
            # build one
            self._typeRegistrar = self.newTypeRegistrar()
        # return it
        return self._typeRegistrar


    # plexus obligations
    @pyre.export
    def help(self, **kwds):
        """
        Hook for the application help system
        """
        # get the package
        import praxis
        # set the indentation
        indent = ' '*4
        # make some space
        self.info.line()
        # get the help header
        for line in praxis._praxis_header.splitlines():
            # and display it
            self.info.line(line)

        # reset the pile of actions
        actions = []
        # get the documented commands
        for uri, name, action, tip in self.pyre_action.pyre_documentedActions():
            # and put them on the pile
            actions.append((name, tip))
        # if there were any
        if actions:
            # figure out how much space we need
            width = max(len(name) for name, _ in actions)
            # introduce this section
            self.info.line('commands:')
            # for each documented action
            for name, tip in actions:
                # show the details
                self.info.line('{}{:>{}}: {}'.format(indent, name, width, tip))
            # some space
            self.info.line()

        # flush
        self.info.log()
        # and indicate success
        return 0


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


    def newDatastoreClient(self):
        """
        Build a connection to the project datastore
        """
        # get the component
        from . import datastore
        # create a connection and return it
        return datastore(name='{.layout.project}_datastore'.format(self))


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


    def newTypeRegistrar(self):
        """
        Instantiate the indexer of data categories
        """
        # get the factory
        from .. support import typeRegistrar
        # build one
        registrar = typeRegistrar(datastore=self.datastore)
        # and return it
        return registrar


    # private data
    _builder = None
    _primer = None
    _idd = None
    _datastore = None
    _typeRegistrar = None


# end of file
