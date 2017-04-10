# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# externals
import os


# administrative
def copyright():
    """
    Return the praxis copyright note
    """
    return meta.copyright

def license():
    """
    Print the praxis license
    """
    return meta.license

def version():
    """
    Return the praxis version
    """
    return meta.version

def credits():
    """
    Print the acknowledgments
    """
    return meta.acknowledgments


def usage(**kwds):
    # print the usage screen
    print(meta.usage)
    # and return
    return


# convenience for interactive explorations
def pg():
    # build an application layout
    cfg = layout()
    # build a db component
    dbc = db.postgres(name="{.project}_db".format(cfg))
    # establish the connection
    dbc.attach()
    # and return the component
    return dbc

# import and publish pyre symbols
from pyre import (
    # protocols, components and traits
    schemata, protocol, component, foundry, properties, constraints, application,
    # decorators
    export, provides,
    # the runtime manager
    executive,
    # db support
    db, records, tabular,
    # miscellaneous packages
    patterns, tracking, units,
)

# fire up
package = executive.registerPackage(name='praxis', file=__file__)
# save the geography
home, prefix, defaults = package.layout()

# access to components
from .components import idd, layout, datastore, plexus, action, command

# and other {praxis} parts
from . import (
    # project meta-data
    meta,
    # my exceptions
    exceptions,
    # auxiliaries
    support,
    # the external file layouts
    ingest,
    # the database schema
    schema,
    # the queries
    queries,
    # the data model
    model,
    # vendors
    vendors,
    # my actions
    actions
)

# end of file
