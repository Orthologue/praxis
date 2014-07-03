# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import pyre


# declaration
class Layout(pyre.shells.layout, family="praxis.layout"):
    """
    A collection of configuration options that define the layout of a praxis deployment
    """


    # public state
    project = pyre.properties.str(default='praxis')
    project.doc = 'the nickname of this deployment'

    iddcfg = pyre.properties.uri(default='file:idd.cfg')
    iddcfg.doc = 'the uri of the idd configuration file'


# end of file 