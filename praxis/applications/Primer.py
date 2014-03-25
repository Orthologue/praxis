# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

"""
Prime certain tables with default values

A notable example of a family of tables that can be primed with default data are tables like
{EmailType} and {PhoneType} that define the acceptable values for the metadata of their
underlying data tables. This practice promotes more thorough schema normalization while
enabling extensibility.
"""


# access the package
import praxis


# app declaration
class Primer(praxis.dbapp):
    """
    Place the static data in the database
    """


    # application obligations
    @praxis.export
    def main(self, *args, **kwds):
        """
        Prime all static data
        """
        # ask my primer to create the default dataset
        records = self.primer.prime(tokenGenerator=self.idd, schema=self.schema)
        # store
        self.db.insert(*records)

        # store the state of {idd}
        self.idd.save(self.iddcfg)

        # and report success
        return 0


# end of file 
