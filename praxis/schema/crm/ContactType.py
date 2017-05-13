# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# superclass
from .. import base


# table declaration
class ContactType(base.type, id='contact_types'):
    """
    A table of the various types of contact information

    This is a helper table that enables multiple pieces of contact information to be imported
    from flat files at the same time. The idea is to provide a hint as to which table must be
    populated with the information provided. Hence, the contact types are tied to the contact
    schema and must be updated as the schema evolves.

    The current primer fills this table with the following values:
        emails, locations, phones, uris
    """


# end of file
