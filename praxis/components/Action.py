# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access the pyre framework
import pyre


# protocol declaration
class Action(pyre.action, family='praxis.actions'):
    """
    Protocol declaration for praxis commands
    """


    @classmethod
    def pyre_contextPath(cls):
        """
        Return an iterable over the starting point for hunting down my actions
        """
        # build a string to uri converter
        uri = cls.uri()
        # first mine, then the ones i inherit from praxis 
        return [ uri.coerce(value='vfs:/praxis'), uri.coerce(value='vfs:/pyre') ]


    @classmethod
    def pyre_contextFolders(cls):
        """
        Return an iterable over portions of my family name
        """
        # spells are in the 'spells' folder
        return [ 'actions' ]


# end of file 
