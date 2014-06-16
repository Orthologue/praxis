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
    # build an application layout
    cfg = layout()
    # build a db component
    dbc = db.postgres(name="{.project}:db".format(cfg))
    # establish the connection
    dbc.attach()
    # and return the component
    return dbc

# import and publish pyre symbols
from pyre import (
    # protocols, components and traits
    schemata, protocol, component, properties,
    # decorators
    export, provides,
    # the runtime manager
    executive,
    # db support
    db, records, tabular,
    # miscellaneous packages
    tracking, units,
)

# fire up
package = executive.registerPackage(name='praxis', file=__file__)
# save the geography
home, prefix, defaults = package.layout()

# access to components
from .components import idd, layout, action, datastore, plexus
from .actions import command

# and other {praxis} parts
from . import (
    # the database schema
    schema,
    # the data model
    model,
    # the queries
    queries,
    # the external file layouts
    ingest,
    # auxiliaries
    support,
)


# end of file 
