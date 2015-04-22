# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# declaration
class PunchParser:
    """
    Extracts employee clock punches from the CATAPULT time report

    The extracted information is kept in a dictionary indexed by the employee id whose values
    are lists of clock-in/clock-out pairs of timestamps
    """


    # exceptions
    from .exceptions import ParsingError


    # interface
    def parse(self, stream, errorlog, warninglog, **kwds):
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

        # reset the pile of errors and warnings
        errors = []
        warnings = []

        # start reading
        for line, text in enumerate(reader):
            # pull in the punch info
            info = text[self.OFFSET_EMPLOYEE].strip()
            clockin = text[self.OFFSET_CLOCKIN].strip()
            clockout = text[self.OFFSET_CLOCKOUT].strip()

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

                # get the package
                import praxis
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
            # now the clock punches
            clockin = datetime.datetime.strptime(clockin, self.TIME_FORMAT)
            clockout = datetime.datetime.strptime(clockout, self.TIME_FORMAT)

            # build the date key
            date = None if clockin is None else clockin.date()

            # check that clock in and clock out happened in the same day
            if date != clockout.date():
                msg = "{}: date mismatch: in: {}, out: {}".format(
                    " ".join(reversed(name)), date, clockout.date())
                # get the package
                import praxis
                # build a locator
                here = praxis.tracking.file(source=stream.name, line=line+1)
                # it's rare but perhaps ok, so it's a warning
                warnings.append(self.ParsingError(description=msg, locator=here))

            # store
            names[eid] = name
            punches[eid][date].newTask(name='in', start=clockin, finish=clockout)

        # if there were any errors
        if errors:
            # check in
            errorlog.line('while parsing the clock punches:')
            # go through them
            for error in errors:
                # and print them out
                errorlog.line(str(error))
            # get the count
            count = len(errors)
            # flush
            errorlog.log('{} error{} total'.format(count, '' if count == 1 else 's'))

        # if there were any warnings
        if warnings:
            # check in
            warninglog.line('while parsing the clock punches:')
            # go through them
            for warning in warnings:
                # and print them out
                warninglog.line(str(warning))
            # get the count
            count = len(warnings)
            # flush
            warninglog.log('{} warning{} total'.format(count, '' if count == 1 else 's'))

        # all done
        return names, punches


    # constants -- for version 3.2.02 of the CATAPULT report
    OFFSET_EMPLOYEE = 6
    OFFSET_CLOCKIN = 10
    OFFSET_CLOCKOUT = 11

    TIME_FORMAT = "%m/%d/%Y %I:%M:%S%p"


# end of file
