# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = vendors/ecrs/model

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Cash.py \
    ChargeAccount.py \
    Coupon.py \
    CreditCard.py \
    DebitCard.py \
    Discount.py \
    GiftCard.py \
    Invoice.py \
    Punches.py \
    Refund.py \
    Task.py \
    Tax.py \
    Tender.py \
    Transaction.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file
