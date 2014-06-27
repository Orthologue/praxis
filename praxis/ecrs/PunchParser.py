# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# declaration
class PunchParser:
    """
    Extracts employee clock punches from the CATAPULT time report

    The extracted information is kept in a dictionary indexed by the employee id whose values
    are lists of clock-in/clock-out pairs of timestamps
    """


    # interface
    def parse(self, stream, **kwds):
        """
        Extract clock-in/clock-out punches from the given {stream}

        The additional {kwds} are passed to the CSV reader without any further processing
        """
        # get the csv package
        import csv
        # the datetime package so we can parse timestamps
        import datetime
        # for {pyre.patterns.vivify}
        import pyre
        # and the clock payload object
        from .. import model

        # build the payload
        names = {}
        punches = pyre.patterns.vivify(levels=2, atom=model.punchlist)
        # create a reader
        reader = csv.reader(stream, **kwds)

        # start reading
        for line in reader:
            # pull in the punch info
            info = line[self.OFFSET_EMPLOYEE]
            clockin = line[self.OFFSET_CLOCKIN]
            clockout = line[self.OFFSET_CLOCKOUT]

            # type conversions
            # first the employee id and name
            rawid, rawname = info.split(None, 1)
            # normalize
            eid = ''.join(rawid.split(',')) # the raw ids have thousands separators...
            name = tuple(rawname.split(',  ')) # the name portion is {last,  first}
            # now the clock punches
            clockin = datetime.datetime.strptime(clockin, self.TIME_FORMAT) if clockin else None
            clockout = datetime.datetime.strptime(clockout, self.TIME_FORMAT) if clockout else None

            # build the date key
            date = None if clockin is None else clockin.date()
            
            # store
            names[eid] = name
            punches[eid][date].append(('in', clockin, clockout))

        # all done
        return names, punches


    # constants -- for version 3.2.02 of the CATAPULT report
    OFFSET_EMPLOYEE = 6
    OFFSET_CLOCKIN = 10
    OFFSET_CLOCKOUT = 11

    TIME_FORMAT = "%m/%d/%Y %I:%M:%S%p"


# end of file
