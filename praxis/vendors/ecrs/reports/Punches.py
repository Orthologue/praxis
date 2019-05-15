# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# declaration
class Punches:
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
    def parse(self, stream, names=None, punches=None, warnings=None, errors=None, **kwds):
        """
        Extract clock-in/clock-out punches from the given {stream}

        The additional {kwds} are passed to the CSV reader without any further processing
        """
        # get the csv package
        import csv
        # the datetime package so we can parse timestamps
        import datetime
        # for my services
        import praxis

        # build the payload: the name
        names = {} if names is None else names
        # and the time punches
        punches = praxis.patterns.vivify(
            levels=2, atom=self.model.punchlist) if punches is None else punches

        # reset the pile of errors and warnings
        errors = [] if errors is None else errors
        warnings = [] if warnings is None else warnings
        # create a reader
        reader = csv.reader(stream, **kwds)

        # start reading
        for line, record in enumerate(reader):
            # pull in the punch info
            info = record[self.OFFSET_EMPLOYEE].strip()
            clockin = record[self.OFFSET_CLOCKIN].strip()
            clockout = record[self.OFFSET_CLOCKOUT].strip()

            # if we couldn't extract all the information we need
            if not (info and clockin and clockout):
                # reset the pile of complaints
                complaints = []
                # if we don't know the employee
                if not info: complaints.append('no employee info')
                # no clock in
                if not clockin: complaints.append('no clock in')
                # no clock out
                if not clockout: complaints.append('no clock out')

                # if we have employee info
                if info:
                    # get the name of the employee
                    _, name = info.split(None, 1)
                    # normalize
                    name = " ".join(reversed(name.split(',  '))) + ': '
                # otherwise
                else:
                    # no name info
                    name = ''

                # if we have clock in info
                if clockin:
                    # we have a date
                    stamp = "on {}: ".format(
                        datetime.datetime.strptime(clockin, self.TIME_FORMAT).date())
                # otherwise
                else:
                    # we don't
                    stamp = ''

                # build the description
                msg = "{}{}{}".format(name, stamp, ", ".join(complaints))

                # build a locator
                here = praxis.tracking.file(source=stream.name, line=line+1)

                # complain
                errors.append(self.ParsingError(description=msg, locator=here))
                # and move
                continue

            # type conversions
            # first the employee id and name
            rawid, rawname = info.split(None, 1)
            # normalize
            eid = ''.join(rawid.split(',')) # the raw ids have thousands separators...
            name = tuple(rawname.split(',  ')) # the name portion is {last,  first}
            # now, attempt to
            try:
                # parse the clock punches
                clockin = datetime.datetime.strptime(clockin, self.TIME_FORMAT)
                clockout = datetime.datetime.strptime(clockout, self.TIME_FORMAT)
            # if something goes wrong
            except ValueError as error:
                # build a locator
                here = praxis.tracking.file(source=stream.name, line=line+1)
                # tell me where the problem is
                raise self.ParsingError(description=str(error), locator=here) from None

            # build the date key
            date = None if clockin is None else clockin.date()

            # check that clock in and clock out happened in the same day
            if date != clockout.date():
                msg = "{}: date mismatch: in: {}, out: {}".format(
                    " ".join(reversed(name)), date, clockout.date())
                # build a locator
                here = praxis.tracking.file(source=stream.name, line=line+1)
                # it's rare but perhaps ok, so it's a warning
                warnings.append(self.ParsingError(description=msg, locator=here))

            # check that the clock out is later than the clock in
            if clockin > clockout:
                msg = "{}: clock out before clock in: in: {}, out: {}".format(
                    " ".join(reversed(name)), clockin, clockout)
                # build a locator
                here = praxis.tracking.file(source=stream.name, line=line+1)
                # complain
                errors.append(self.ParsingError(description=msg, locator=here))

            # store
            names[eid] = name
            punches[eid][date].newTask(name='in', start=clockin, finish=clockout)

        # all done
        return names, punches, warnings, errors


    def filter(self, stream, **kwds):
        """
        Throw away everything except the employee name and punch info; also keep the zeroth column
        where we record downstream updates of the record when the mispunch log is applied
        """
        # get the csv package
        import csv
        # create a reader
        reader = csv.reader(stream, **kwds)

        # start reading
        for record in reader:
            # extract what we care about
            status = record[self.OFFSET_STATUS].strip()
            info = record[self.OFFSET_EMPLOYEE].strip()
            clockin = record[self.OFFSET_CLOCKIN].strip()
            clockout = record[self.OFFSET_CLOCKOUT].strip()
            # build an empty list with the right length
            filtered = ['']*len(record)
            # populate
            filtered[self.OFFSET_STATUS] = status
            filtered[self.OFFSET_EMPLOYEE] = info
            filtered[self.OFFSET_CLOCKIN] = clockin
            filtered[self.OFFSET_CLOCKOUT] = clockout
            # make the filtered record available
            yield filtered

        # all done
        return


    # constants -- for version 3.2.02 of the CATAPULT report
    OFFSET_STATUS = 0
    OFFSET_EMPLOYEE = 6
    OFFSET_CLOCKIN = 10
    OFFSET_CLOCKOUT = 11

    TIME_FORMAT = "%m/%d/%Y %I:%M:%S%p"


# end of file
