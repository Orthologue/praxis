# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis
# foreign tables
from .. import crm
from .InvoiceType import InvoiceType


# table declaration
class Invoice(praxis.db.table, id='invoices'):
    """
    Encapsulation of a financial transaction between entities
    """


    # data layout
    id = praxis.db.str().primary()
    kind = praxis.db.reference(key=InvoiceType.type).notNull()
    description = praxis.db.str().notNull()

    # the two entities involved in this transaction
    payer = praxis.db.reference(key=crm.entity.entity)
    payee = praxis.db.reference(key=crm.entity.entity)

    # the entity recording the transaction
    scribe = praxis.db.reference(key=crm.entity.entity)

    # start and stop dates
    opened = praxis.db.time().notNull()
    closed = praxis.db.time(default=praxis.db.null)


# end of file
