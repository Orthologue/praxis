# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# types
from .InvoiceType import InvoiceType as invoiceType
from .ItemType import ItemType as itemType
from .TenderType import TenderType as tenderType

# atoms
from .Invoice import Invoice as invoice
from .InvoiceItem import InvoiceItem as invoiceItem
from .Item import Item as item


# table groups
# types
typeTables = (
    invoiceType, itemType, tenderType,
)

# atoms
atomTables = (
    invoice, invoiceItem, item,
)

# attributes
attributeTables = (
)

# relations
relationTables = (
)

# the table list, sorted by dependency
tables = typeTables + atomTables + attributeTables + relationTables


# end of file
