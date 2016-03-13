# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# superclass
from .Type import Type


# table declaration
class ContactType(Type, id='contact_types'):
    """
    A table of the various types of contact information

    This is a helper table that enables multiple pieces of contact information to be imported
    from flat files at the same time. The idea is to provide a hint as to which table must be
    populated with the information provided. Hence, the contact types are tied to the contact
    schema and must be updated as the schema evolves.
    """


# end of file
