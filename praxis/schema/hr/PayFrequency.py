# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# access to the framework
import praxis


# table declaration
class PayFrequency(praxis.db.table, id='pay_frequencies'):
    """
    A table of the various compensation frequencies

    The current primer fills this table with the following values:
        weekly, biweekly, monthly, quarterly, annually
    """


    # data layout
    frequency = praxis.db.str().primary()
    description = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.frequency}: {0.description}".format(self)


# end of file
