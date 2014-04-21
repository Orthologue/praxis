# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
        # and pull in the {defaultdict}
        import collections

        # build the payload
        names = {}
        punches = collections.defaultdict(list)
        # create a reader
        reader = csv.reader(stream, **kwds)

        # start reading
        for line in reader:
            # pull in the punch info
            raw = line[self.OFFSET_RAW]
            clockin = line[self.OFFSET_CLOCKIN]
            clockout = line[self.OFFSET_CLOCKOUT]

            # type conversions
            # first the employee id and name
            rawid, rawname = raw.split(None, 1)
            # normalize
            eid = ''.join(rawid.split(','))
            name = ' '.join(reversed(rawname.split(',  ')))
            # now the clock punches
            clockin = datetime.datetime.strptime(clockin, self.TIME_FORMAT) if clockin else None
            clockout = datetime.datetime.strptime(clockout, self.TIME_FORMAT) if clockout else None
            
            # store
            names[eid] = rawname
            punches[eid].append((clockin, clockout))

        # all done
        return names, punches


    # constants -- for version 3.2.02 of the CATAPULT report
    OFFSET_RAW = 6
    OFFSET_CLOCKIN = 10
    OFFSET_CLOCKOUT = 11

    TIME_FORMAT = "%m/%d/%Y %I:%M:%S%p"


# end of file
