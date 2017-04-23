# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# declaration
class Daily:
    """
    Extract sales performance from a variety of daily reports
    """


    # exceptions
    from ..exceptions import ParsingError


    # interface
    def lastFourWeeks(self, stream, table=None, warnings=None, errors=None, **kwds):
        """
        Extract daily department performance for the last four weeks

        Known to work with
            report version 5.2, Catapult catalog id IT-212
        """
        # get my services
        import praxis
        # and the externals
        import csv, datetime, decimal

        # one day
        day = datetime.timedelta(days=1)
        # initialize the result table
        table = praxis.patterns.vivify(levels=2, atom=decimal.Decimal) if table is None else table

        # create a reader
        reader = csv.reader(stream, **kwds)

        # start reading
        for line, record in enumerate(reader):
            # get the department
            department = record[self.OFFSET_DEPARTMENT]
            # get the last day of this week
            last = datetime.datetime.strptime(record[self.OFFSET_DATE], self.DATE_FORMAT).date()
            # rewind to the beginning of the week
            date = last - 6*day
            # we have seven days of data per line
            for offset in range(7):
                # get the sales for day
                raw = record[self.OFFSET_SALES + offset]
                # skip the dollar sign, split on the comma, and assemble
                sales = decimal.Decimal(''.join(raw[1:].split(',')))
                # store
                table[department][date + offset*day] = sales

        # return
        return table, warnings, errors


    # constants
    OFFSET_DEPARTMENT = 17
    OFFSET_WEEK = 18
    OFFSET_DATE = 19
    OFFSET_SALES = 20

    DATE_FORMAT = '%m/%d/%Y'


# end of file
