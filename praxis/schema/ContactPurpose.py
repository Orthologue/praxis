# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis


# table declaration
class ContactPurpose(praxis.db.table, id='contact_purposes'):
    """
    A table of the intended use of the contact information

    The current primer fills this table with the following values:
        personal, work, info, shipping, billing
    """


    # data layout
    purpose = praxis.db.str().primary()
    description = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.purpose}: {0.description}".format(self)


# end of file
