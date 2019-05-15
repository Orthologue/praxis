# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# get the db support
from .. import db

# literals, for convenience
null = db.null
default = db.default

# abstract base tables
from .Type import Type as type

# mix-ins
from .Temporary import Temporary as temporary

# end of file
