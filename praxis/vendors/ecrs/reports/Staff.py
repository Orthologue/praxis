# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# declaration
class Staff:
    """
    Extracts employee clock punches from the CATAPULT time report

    The extracted information is kept in a dictionary indexed by the employee id whose values
    are lists of clock-in/clock-out pairs of timestamps
    """


    # exceptions
    from ..exceptions import ParsingError
    # types
    from .. import model


    # interface
    def parse(self, stream, names=None, warnings=None, errors=None, **kwds):
        """
        Extract employee information from the corresponding ECRS report

        The additional {kwds} are passed to the CSV reader without any further processing
        """
        # get the csv package
        import csv
        # for my services
        import praxis

        # build the payload
        names = {} if names is None else names
        # reset the pile of errors and warnings
        errors = [] if errors is None else errors
        warnings = [] if warnings is None else warnings
        # create a reader
        reader = csv.reader(stream, **kwds)

        # start reading
        for line, record in enumerate(reader):
            pass

        # all done
        return names, warnings, errors


    # constants -- for version 3.2.02 of the CATAPULT report
    OFFSET_STORE = 19
    OFFSET_EID = 20
    OFFSET_LAST = 21
    OFFSET_FIRST = 22
    OFFSET_MIDDLE = 23
    OFFSET_ALIAS = 24
    OFFSET_EMPLOYEE_ID = 25
    OFFSET_AUTH = 26
    OFFSET_TITLE = 27
    OFFSET_SALES = 28
    OFFSET_STATUS = 29
    OFFSET_PHONE = 30


# end of file
