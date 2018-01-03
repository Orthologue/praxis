# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = schema/sales

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Invoice.py \
    InvoiceItem.py \
    InvoiceType.py \
    Item.py \
    ItemType.py \
    TenderType.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file
