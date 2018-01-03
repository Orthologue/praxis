# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# externals
import os


# administrative
def copyright():
    """
    Return the praxis copyright note
    """
    # pull and return the meta-data
    return meta.copyright


def license():
    """
    Print the praxis license
    """
    # pull and return the meta-data
    return meta.license


def version():
    """
    Return the praxis version
    """
    # pull and return the meta-data
    return meta.version


def built():
    """
    Return the build time
    """
    # pull and return the meta-data
    return meta.date


def credits():
    """
    Print the acknowledgments
    """
    # pull and return the meta-data
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
    patterns, primitives, tracking, units,
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
    # various pieces of hardware
    hardware,
    # vendors
    vendors,
    # my actions
    actions
)

# end of file
