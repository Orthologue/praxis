# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import praxis


# table declaration
class ContactType(praxis.db.table, id='contact_types'):
    """
    A table of the various types of contact information

    This is a helper table that enables multiple pieces of contact information to be imported
    from flat files at the same time. The idea is to provide a hint as to which table must be
    populated with the information provided. Hence, the contact types are tied to the contact
    schema and must be updated as the schema evolves.
    """

    # data layout
    id = praxis.db.str().primary()
    description = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.id}: {0.description}".format(self)


# end of file 
