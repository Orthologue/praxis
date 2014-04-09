# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import os


# geography
def home():
    """
    Return the package installation directory
    """
    return os.path.dirname(__file__)

def prefix():
    """
    Compute the location of the {praxis} installation
    """
    return os.path.abspath(os.path.join(home(), os.path.pardir, os.path.pardir))

def defaults():
    """
    Compute the location of the package configuration files
    """
    return os.path.abspath(os.path.join(prefix(), 'defaults'))

    
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
from pyre import executive, addPackageConfiguration

# db support
from pyre import db, records, tabular

# miscellaneous packages
from pyre import tracking, units

# fire up
home, prefix, defaults = addPackageConfiguration(namespace='praxis', file=__file__)

# access to the default shells and other components
from .components import app, dbapp, idd
# the database schema
from . import schema
# the queries
from . import queries
# the external file layouts
from . import ingest
# auxiliaries
from . import support
# default application bases
from . import applications


# end of file 
