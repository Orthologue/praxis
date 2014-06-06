# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import pyre
# and some of my parts
from .. import compliance


# declaration
class Application(pyre.application, family="praxis.shells.application"):
    """
    The base class for {praxis} applications
    """

    
    # public state
    jurisdiction = compliance.jurisdiction(default='us.california')
    jurisdiction.doc = 'compliant calculators for the default company jurisdiction'


# end of file 
