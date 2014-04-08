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


# package bootstrapping code
def boot():
    # bail if {pyre} is running in some special mode
    if not executive: return

    # get the fileserver
    fileserver = executive.fileserver
    # and the nameserver
    nameserver = executive.nameserver

    # turn the configuration path into a file node
    cfg = fileserver.local(root=defaults()).discover()
    # attach it under the {praxis} namespace
    fileserver['praxis/system'] = cfg

    # get the configuration path
    cfgpath = nameserver['pyre.configpath']

    # build the uri for the package configuration files
    uri = executive.uri().coerce("vfs:/praxis/system")
    # add it to the configuration path
    cfgpath.append(uri)

    # all done
    return
    

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
boot()

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
