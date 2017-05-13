# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# access to the framework
import praxis
# access to the table of entities
from .. import crm


# table declaration
class Employer(praxis.db.table, id='employers'):
    """
    Information about employers
    """

    employer = praxis.db.reference(key=crm.entity.entity).primary()
    employer.doc = "the entity whose attributes these are"

    # tax id
    tin = praxis.db.str().notNull()
    tin.doc = "the employer's tax id"


# end of file
