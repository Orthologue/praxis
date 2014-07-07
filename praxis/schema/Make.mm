# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = schema

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Company.py \
    ContactPurpose.py \
    ContactType.py \
    Email.py \
    Employment.py \
    EmploymentType.py \
    Entity.py \
    EntityEmail.py \
    EntityLocation.py \
    EntityPhone.py \
    EntityType.py \
    EntityURI.py \
    Item.py \
    ItemType.py \
    Location.py \
    PayType.py \
    PayFrequency.py \
    Person.py \
    Phone.py \
    PhoneType.py \
    URI.py \
    URIType.py \
    Temporary.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file
