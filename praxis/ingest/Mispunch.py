# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import re
# framework
import praxis


# class declaration
class Mispunch:
    """
    Importer of mispunches from a log file
    """


    # interface
    def read(self, stream=None, uri=None, **kwds):
        """
        Load the information in {stream} or {uri} into a collection of records
        """
        # create a reader
        csv = praxis.records.csv()
        # build a reader and return it
        return csv.immutable(layout=self.mispunch, stream=stream, uri=uri, **kwds)


    # implementation details
    # the layout of the file
    class mispunch(praxis.records.record):
        # the fields
        status = praxis.records.bool()
        id = praxis.records.str()
        first = praxis.records.str()
        last = praxis.records.str()

        date = praxis.records.date()
        date.format = "%Y-%m-%d"

        start = praxis.records.time()
        start.format = "%I:%M %p"

        lunchOut = praxis.records.time()
        lunchOut.aliases.add("lunch out")
        lunchOut.format = "%I:%M %p"

        lunchIn = praxis.records.time()
        lunchIn.aliases.add("lunch in")
        lunchIn.format = "%I:%M %p"

        end = praxis.records.time()
        end.format = "%I:%M %p"


        @praxis.records.converter(traits=[first, last])
        def stripper(value):
            return value.strip()


# end of file
