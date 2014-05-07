# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import os

# convenience for interactive explorations
def pg():
    # build a db component
    dbc = db.postgres(name="praxis:db")
    # establish the connection
    dbc.attach()
    # and return the component
    return dbc

# import and publish pyre symbols
# protocols, components and traits
from pyre import schemata, protocol, component, properties
# decorators
from pyre import export, provides
# the runtime manager
from pyre import executive

# db support
from pyre import db, records, tabular

# miscellaneous packages
from pyre import tracking, units

# fire up
package = executive.registerPackage(name='praxis', file=__file__)
# save the geography
home = package.home
prefix = package.prefix
defaults = package.defaults

# access to the default shells and other components
from .components import app, dbapp, idd
# the database schema
from . import schema
# the data model
from . import model
# the queries
from . import queries
# the external file layouts
from . import ingest
# auxiliaries
from . import support
# default application bases
from . import applications


# end of file 
