# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = schema/crm

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Company.py \
    ContactPurpose.py \
    ContactType.py \
    Email.py \
    Entity.py \
    EntityEmail.py \
    EntityLocation.py \
    EntityPhone.py \
    EntityType.py \
    EntityURI.py \
    Location.py \
    Person.py \
    Phone.py \
    PhoneType.py \
    URI.py \
    URIType.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file
