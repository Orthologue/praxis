# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import csv, datetime, itertools, re, operator
# get the package
import praxis


# the action
class Payroll(praxis.command, family='praxis.actions.payroll'):
    """
    Payroll support
    """


    # public state
    payday = praxis.properties.date(default=None, format='%Y%m%d')
    payday.doc = 'the pay period to process'

    month = praxis.properties.date(default='201505', format='%Y%m')
    month.doc = 'show hours worked during this month'

    start = praxis.properties.date(default=None, format='%Y%m%d')
    start.doc = 'the beginning of the period of interest'

    end = praxis.properties.date(default=None, format='%Y%m%d')
    end.doc = 'the end of the period of interest'

    name = praxis.properties.strings(default='.*')
    name.doc = 'show only information relevant for employees whose names match this regex'

    details = praxis.properties.bool(default=False)
    details.doc = 'controls whether to show the punch clock details'

    daily = praxis.properties.bool(default=False)
    daily.doc = 'controls whether to show daily summary'

    jurisdiction = praxis.compliance.jurisdiction(default='us.california')
    jurisdiction.doc = 'compliant calculators for the company jurisdiction'


    # behaviors
    @praxis.export(tip='classify the hours worked in a given pay period')
    def hours(self, plexus, **kwds):
        """
        Parse ECRS timecards for the pay period specified by the given payday
        """
        # find the data set for the requested pay period
        payday, node = self.selectPayday(plexus=plexus)
        # check
        if node is None:
            # we were unable to locate a matching pay date
            plexus.error.log("unable to locate time cards for payday {.payday}".format(self))
            # all done
            return 1

        # let the user know what we are doing
        plexus.info.log('parsing clock punches from {!r}'.format(str(node.uri)))

        # build the employee index
        employees = {}
        # build the punch table
        punches = praxis.patterns.vivify(levels=2, atom=praxis.vendors.ecrs.model.punchlist)
        # initialize the event piles
        errors = [] # parsing errors
        warnings = [] # parsing warnings
        # make a punch parser
        parser = praxis.vendors.ecrs.reports.punches()
        # open the timecards
        with node.open() as stream:
            # parse the input stream
            parser.parse(stream=stream, names=employees, punches=punches,
                         warnings=warnings, errors=errors)
        # if there were any errors
        if errors:
            # check in
            plexus.error.line('while parsing the clock punches:')
            # go through them
            for error in errors:
                # and print them out
                plexus.error.line(str(error))
            # get the count
            count = len(errors)
            # flush
            plexus.error.log('{} error{} total'.format(count, '' if count == 1 else 's'))

        # if there were any warnings
        if warnings:
            # check in
            plexus.warning.line('while parsing the clock punches:')
            # go through them
            for warning in warnings:
                # and print them out
                plexus.warning.line(str(warning))
            # get the count
            count = len(warnings)
            # flush
            plexus.warning.log('{} warning{} total'.format(count, '' if count == 1 else 's'))

        # setup a counter increment
        day = datetime.timedelta(days=1)

        # compute the pay period assuming it's the fourteen days that end on {payday}
        payend = payday
        paystart = payend - 13*day

        # figure out the pay period covered by the data set
        datastart, dataend = self.payperiod(data=punches)
        plexus.info.line('pay period:')
        plexus.info.line('    deduced: {} to {}'.format(paystart, payend))
        plexus.info.line('  retrieved: {} to {}'.format(datastart, dataend))
        plexus.info.log()

        # start
        print("Hours worked:")

        # backup to the Monday of the earliest week
        start = paystart

        # the output format
        hfmt = "{:5.2f}"
        fmt = " | ".join(["{:5} "*3]*2)
        # set up the employee name regex
        regex = re.compile("|".join(name.lower() for name in self.name))

        # for each employee
        for eid, name in sorted(employees.items(), key=operator.itemgetter(1)):
            # build the employee's full name
            fullname = ', '.join(name)
            # should we skip this employee?
            if not regex.search(fullname.lower()): continue
            # get the punches
            timecard = punches[eid]

            # classify the hours worked
            hours = self.jurisdiction.overtime(start=start, workweeks=2, timecard=timecard)
            # tally them
            rawRegular, rawSesqui, rawDouble = map(sum, zip(*hours))

            # repeat the calculation with the new streaming method used by the attendance
            # detail generator
            new = self.jurisdiction.overtime2(start=start, workweeks=2, timecard=timecard)
            # tally them; this looks different from the reduction above because {overtime2}
            # injects the work day in the stream as well, so we have to peel that off
            newRegular, newSesqui, newDouble = map(sum, zip(*(r[1] for r in new)))

            # compare the two to make sure we have no bugs
            assert (rawRegular - newRegular) < 1/3600
            assert (rawSesqui - newSesqui) < 1/3600
            assert (rawDouble - newDouble) < 1/3600

            # repeat while enforcing the legally mandated breaks
            breaks = self.jurisdiction.breaks(start=start, workweeks=2, timecard=timecard)
            # tally them
            brkRegular, brkSesqui, brkDouble = map(sum, zip(*breaks))

            # compute the discrepancy to get a feel for the cost of missing breaks
            dRegular  = rawRegular - brkRegular
            dSesqui  = rawSesqui - brkSesqui
            dDouble  = rawDouble - brkDouble

            # put the report together
            line = fmt.format(
                hfmt.format(rawRegular) if rawRegular else "  -  ",
                hfmt.format(rawSesqui) if rawSesqui else "  -  ",
                hfmt.format(rawDouble) if rawDouble else "  -  ",
                # brkRegular, brkSesqui, brkDouble,
                hfmt.format(dRegular) if dRegular else "  -  ",
                hfmt.format(dSesqui) if dSesqui else "  -  ",
                hfmt.format(dDouble) if dDouble else "  -  ",
            )

            # show me
            print("{:>25} :  {}".format(fullname, line))

            # if we are not going to show details
            if not self.daily and not self.details:
                # carry on
                continue
            # otherwise, set up a loop over the punches
            for workday in sorted(timecard):
                # format the date
                day = workday.strftime('%a, %m/%d')
                # show a summary
                print("    {}: {:.2f}".format(day, timecard[workday].hours))
                # skip if the user didn't ask for a daily log
                if not self.details: continue
                # and the individual punches
                for task in timecard[workday]:
                    print('        {} to {}, hours: {:.2f}'.format(
                        task.start.time(), task.finish.time(), task.hours))

        # all done
        return 0


    @praxis.export(tip='assess the impact of employees not taking breaks')
    def breaks(self, plexus, **kwds):
        """
        Compute the impact of missing/short half hour breaks
        """
        # units
        day = datetime.timedelta(1)
        # get the jurisdiction
        js = self.jurisdiction
        # get the time data
        dataset = self.punches(plexus=plexus, latest=True)
        # go through the time cards
        for eid, (last, first), punches in dataset:
            # initialize the instance count
            instances = 0
            # assemble the name of the output file
            outfile = ''.join(''.join((last, first)).split()) + '-pay.csv'
            # open it
            writer = csv.writer(open(outfile, 'w'))
            # leave behind the employee name
            writer.writerow(("Employee:", last, first))

            # write my headers
            writer.writerow(("Pay Period", "", "Raw", "", "Breaks", "", "Difference", ""))
            writer.writerow(("Start", "End",
                             "Regular", "Overtime", "Regular", "Overtime", "Regular", "Overtime"))

            # my accumulators
            rawRegular, rawSesqui, rawDouble = 0,0,0
            brkRegular, brkSesqui, brkDouble = 0,0,0
            # and for each available time card
            for payday in sorted(punches, reverse=True):
                # get the tasks
                tasks = punches[payday]
                # compute the start of the pay period
                start = payday - 13*day
                # initialize the row
                record = [start,payday]
                # compute the raw hours worked this date
                raw = js.overtime(start=start, workweeks=2, timecard=tasks)
                # sum up
                regularR, sesquiR, doubleR = map(sum, zip(*raw))
                # save in the current row
                record += ["{:.2f}".format(regularR), "{:.2f}".format(sesquiR)]
                # and update the raw accumulators
                rawRegular += regularR
                rawSesqui += sesquiR
                rawDouble += doubleR

                # repeat for hours adjusted for the missing breaks
                breaks = js.breaks(start=start, workweeks=2, timecard=tasks)
                # sum up
                regularB, sesquiB, doubleB = map(sum, zip(*breaks))
                # save in the current row
                record += ["{:.2f}".format(regularB), "{:.2f}".format(sesquiB)]
                # and update the raw accumulators
                brkRegular += regularB
                brkSesqui += sesquiB
                brkDouble += doubleB

                # compute the deltas
                regularD = regularR - regularB
                sesquiD = sesquiR - sesquiB
                doubleD = doubleR - doubleB

                # save the difference
                record += ["{:.2f}".format(regularD), "{:.2f}".format(sesquiD)]

                # update the instance count
                if regularD > 0.1 or sesquiD > 0.1: instances += 1

                # and record
                writer.writerow(record)

            # show me
            print(
                "{name:25}: {instances:3d}: {reg:6.2f} {ovr:6.2f} {dbl:6.2f}".format(
                    name = '{}, {}'.format(last, first),
                    instances = instances,
                    reg = rawRegular - brkRegular,
                    ovr = rawSesqui - brkSesqui,
                    dbl = rawDouble - brkDouble))

        return 0


    @praxis.export(tip='collect the clock punches of select employees')
    def record(self, plexus, **kwds):
        """
        Collect all the clock punches of select employees in separate files
        """
        # get the data set
        dataset = self.punches(plexus=plexus, latest=False)
        # get the selected employees and their timecards
        for eid, (last, first), punches in dataset:
            # assemble the name of the output file
            name = ''.join(''.join((last, first)).split()) + '-time.csv'
            # make a CSV writer
            writer = csv.writer(open(name, 'w'))
            # leave behind the employee name in the first row
            writer.writerow((last, first))

            # focus on the paydays that are relevant for this employee
            for payday in sorted(punches, reverse=True):
                # get the days worked during this pay period
                entries = punches[payday]
                # and go through them in order
                for date in sorted(entries, reverse=True):
                    # go through each task
                    for task in entries[date]:
                        # compute the difference and convert into hours
                        delta = (task.finish - task.start).total_seconds() / 3600
                        # write a line in the file
                        writer.writerow((date, task.start, task.finish, "{:.2f}".format(delta)))

        # all done
        return 0


    @praxis.export(tip='generate a document with punch clock detail for a given pay period')
    def detail(self, plexus, **kwds):
        """
        Generate a LaTeX document with the punch clock details for a given pay period
        """
        # grab the folder with my data store; it's guaranteed to be there by the application
        # boot process
        etc = plexus.pfs["etc"]
        # grab the level below
        etc.discover(levels=1)
        # get the folder with the timecards
        tex = etc["tex"].discover()
        # get the include and graphics folders
        include = str(tex["include"].uri)
        graphics = str(tex["graphics"].uri)

        # get the timecards
        timecards = self.timecards(plexus=plexus)
        # resolve the time period
        paystart, payend = self.resolveInterval(plexus=plexus, timecards=timecards, latest=True)
        # get the time card dataset
        dataset = self.punches(plexus=plexus, timecards=timecards, latest=True)

        # create the file
        doc = open("{:%Y%m%d}-detail.tex".format(payend), "w")

        # the preamble
        preamble = [
            "% -*- LaTeX -*-",
            "% -*- coding: utf-8 -*-",
            "%",
            "% michael a.g. aïvázis",
            "% urban radish",
            "% (c) 1998-2016 all rights reserved",
            "%",
            "% adjust the include path",
            "\makeatletter",
            "\providecommand*{\input@path}{}",
            "\edef\input@path{{{{{include}/}}\input@path}}".format(include=include),
            "\makeatother",
            "",
            "% document support",
            "\\documentclass{praxis}",
            "",
            "% adjust the graphics path",
            "\graphicspath{{{{{graphics}/}}}}".format(graphics=graphics),
            "",
            "% setup",
            "\\meta{",
              "% pay period",
              "payperiodStart = {{{:%B %d, %Y}}},".format(paystart),
              "payperiodEnd = {{{:%B %d, %Y}}},".format(payend),
              "}",
            "",
            "% the document",
            "\\begin{document}",
            "",
        ]
        print('\n'.join(preamble), file=doc)

        # for each employee
        for eid, (last, first), punches in dataset:
            # the attendance header
            header = [
                "",
                "% attendance for {first} {last}".format(first=first, last=last),
                "\\begin{{attendance}}{{{first} {last}}}".format(first=first, last=last),
                ]
            # inject it
            print('\n'.join(header), file=doc)

            # get the punches
            timecard = punches[payend]
            # prime the streaming overtime calculator
            overtime = self.jurisdiction.overtime2(start=paystart, workweeks=2, timecard=timecard)
            # initialize the counter of work days
            workdays = 0
            # go through them
            for date, (reg, ovr, dbl) in overtime:
                # increment the workday counter
                workdays += 1
                # build date args
                datearg = "{{{0.day}}}{{{0.month}}}{{{0.year}}}".format(date)
                # initialize the content
                line = []

                # colorize even rows
                if workdays % 2 == 0:
                    line += [
                        "% colorize",
                        "\\rowcolor[gray]{.95}",
                        ]

                # prime the line
                line += [
                    "  % punches",
                    "  \\simpledate\\formatdate{} &".format(datearg),
                    "  \\shortdayofweekname{} &".format(datearg),
                    ]

                # get the tasks
                tasks = timecard[date]

                # if there are no tasks
                if not tasks:
                    # wrap up this day
                    line += [
                        " & & & & & & \\\\" + ("\\midrule " if workdays % 7 == 0 else "")
                    ]
                    # inject
                    print('\n'.join(line), file=doc)
                    # and move on
                    continue

                # if there are two tasks
                if len(tasks) == 2:
                    # unpack
                    ein = "{{{0.hour}}}{{{0.minute}}}{{{0.second}}}".format(tasks[0].start)
                    lin = "{{{0.hour}}}{{{0.minute}}}{{{0.second}}}".format(tasks[0].finish)
                    lout = "{{{0.hour}}}{{{0.minute}}}{{{0.second}}}".format(tasks[1].start)
                    eout = "{{{0.hour}}}{{{0.minute}}}{{{0.second}}}".format(tasks[1].finish)

                    # adjust
                    line += [
                        "\\formattime{} &".format(ein),
                        "\\formattime{} &".format(lin),
                        "\\formattime{} &".format(lout),
                        "\\formattime{} &".format(eout),
                        ]
                # if there is only one task
                elif len(tasks) == 1:
                    # unpack
                    ein = "{{{0.hour}}}{{{0.minute}}}{{{0.second}}}".format(tasks[0].start)
                    eout = "{{{0.hour}}}{{{0.minute}}}{{{0.second}}}".format(tasks[0].finish)

                    # adjust
                    line += [
                        "\\formattime{} &".format(ein),
                        "&",
                        "&",
                        "\\formattime{} &".format(eout),
                        ]
                # if there are more than 2
                if len(tasks) > 2:
                    # raise a firewall
                    plexus.firewall.log(
                        "{2} {1} has more than two tasks on {0}".format(date, *name))

                # format the hours
                reg = "{:.2f}".format(reg) if reg else ''
                ovr = "{:.2f}".format(ovr) if ovr else ''
                dbl = "{:.2f}".format(dbl) if dbl else ''
                # render the hour classifications
                line += [
                    "{} & {} & {}".format(reg, ovr, dbl)
                    ]

                # wrap up this day
                line += [
                    "\\\\" + ("\\midrule " if workdays % 7 == 0 else "")
                    ]
                # inject
                print('\n'.join(line), file=doc)

            # classify the hours worked
            hours = self.jurisdiction.overtime(start=paystart, workweeks=2, timecard=timecard)
            # and add them up
            reg, ovr, dbl = map(sum, zip(*hours))
            # format them
            reg = "{:.2f}".format(reg) if reg else ""
            ovr = "{:.2f}".format(ovr) if ovr else ""
            dbl = "{:.2f}".format(dbl) if dbl else ""

            # create the summary
            summary = [
                "\\multicolumn{5}{c}{} & ",
                "\\bfseries{{Total}}: & {} & {} & {}".format(reg, ovr, dbl)
                ]
            # inject it
            print('\n'.join(summary), file=doc)

            # the attendance footer
            footer = [
                "\\end{attendance}",
                "",
                ]
            # inject it
            print('\n'.join(footer), file=doc)


        # wrap up
        postamble = [
            "% all done",
            "\\end {document}",
            "",
            "% end of file",
            ]
        print('\n'.join(postamble), file=doc)

        # all done
        return 0


    # implementation details
    def payperiod(self, data):
        """
        Compute the time span over which we are tabulating hours worked
        """
        # create a set of all punch dates by all employees
        dates = { date for punches in data.values() for date in punches }
        return min(dates), max(dates)


    def timecards(self, plexus):
        """
        Search the archive for files with time cards
        """
        # grab the folder with my data store; it's guaranteed to be there by the application
        # boot process
        etc = plexus.pfs["etc"]
        # grab the level below
        etc.discover(levels=1)
        # get the folder with the timecards
        folder = etc["timecards"].discover()
        # filter for the contents of interest
        contents = folder.find(pattern=self.TIMECARDS)
        # collect all entries that look like time cards
        timecards = sorted(((datetime.date(year=int(match.group('year')),
                                           month=int(match.group('month')),
                                           day=int(match.group('day'))),
                             node)
                            for node, match in contents))
        # if there aren't any
        if not timecards:
            # complain
            raise plexus.error.log('could not find any time cards in {!r}'.format(str(folder.uri)))

        # otherwise, return them

        return timecards


    def selectRange(self, plexus, timecards, latest=True):
        """
        Narrow down the time card dataset according to the user specifications
        """
        # units
        day = datetime.timedelta(1)
        # payroll happens biweekly
        # MGA: pull this from the client configuration
        payperiod = 14*day
        # resolve the time interval of interest
        start, end = self.resolveInterval(plexus=plexus, timecards=timecards, latest=latest)

        # otherwise, loop over the available time cards
        for date, node in timecards:
            # if the time interval has a left edge and the payday is not after it
            if date < start:
                # skip it
                continue
            # if the time interval has a right edge and the payday is more than one pay period
            # in the future
            if date - end >= payperiod:
                # skip it
                continue

            # otherwise, it is within range
            yield date, node

        # all done
        return


    def selectPayday(self, plexus):
        """
        Identify the timecards for the pay period specified by the user
        """
        # N.B.: the logic below assumes that {timecards} are sorted by date

        # grab the time cards
        timecards = self.timecards(plexus=plexus)
        # get the payday
        payday = self.payday
        # if the user didn't specify one
        if payday is None:
            # interpret this as a request for the latest available
            payday, node = timecards[-1]
        # otherwise
        else:
            # duration
            day = datetime.timedelta(1)
            # go through the time cards
            for enddate, node in timecards:
                # back up to the beginning of the pay period
                startdate = enddate - 13*day
                # find the first one that contains the given date
                if payday >= startdate and payday <= enddate:
                    # remember the enddate
                    payday = enddate
                    # and bail
                    break
            # otherwise
            else:
                # we couldn't find it; what went wrong?
                return None, None

        # adjust the payday
        self.payday = payday
        # all done
        return payday, node


    def punches(self, plexus, timecards=None, latest=True, warnings=None, errors=None):
        """
        Load the clock punches from the sequence of {date, vnode} pairs
        """
        # build the employee index
        employees = {}
        # force initialization of the timecards
        if timecards is None: timecards = self.timecards(plexus=plexus)
        # and the punch data
        index = praxis.patterns.vivify(levels=3, atom=praxis.vendors.ecrs.model.punchlist)

        # initialize the event piles
        errors = [] if errors is None else errors # parsing errors
        warnings = [] if warnings is None else warnings # parsing warnings

        # make a punch parser
        parser = praxis.vendors.ecrs.reports.punches()

        # go through the timecard specs
        for payperiod, node in self.selectRange(plexus=plexus, timecards=timecards, latest=latest):
            # build the punch table
            punches = praxis.patterns.vivify(levels=2, atom=praxis.vendors.ecrs.model.punchlist)
            # open the file
            with node.open() as stream:
                # parse
                parser.parse(stream = stream,
                             names = employees, punches = punches,
                             warnings = warnings, errors = errors)
            # transfer the data for each employee
            for eid in punches:
                # by injecting the pay period between the employee and the punches
                index[eid][payperiod] = punches[eid]

        # if there were any errors
        if errors:
            # check in
            plexus.error.line('while parsing the clock punches:')
            # go through them
            for error in errors:
                # and print them out
                plexus.error.line(str(error))
            # get the count
            count = len(errors)
            # flush
            plexus.error.log('{} error{} total'.format(count, '' if count == 1 else 's'))

        # if there were any warnings
        if warnings:
            # check in
            plexus.warning.line('while parsing the clock punches:')
            # go through them
            for warning in warnings:
                # and print them out
                plexus.warning.line(str(warning))
            # get the count
            count = len(warnings)
            # flush
            plexus.warning.log('{} warning{} total'.format(count, '' if count == 1 else 's'))

        # now, build the employee name filter
        namefilter = re.compile('|'.join(name.lower() for name in self.name))
        # identify the employees of interest
        eids = tuple(
            eid
            for eid, name in sorted(employees.items(), key=operator.itemgetter(1))
            if namefilter.search("{first} {last}".format(last=name[0], first=name[1]).lower())
            )

        # for each employee in the target group
        for eid in eids:
            # send off the employee id, name and time cards
            yield eid, employees[eid], index[eid]

        # all done
        return


    def resolveInterval(self, plexus, timecards, latest):
        """
        Compute the time interval of interest based on the user input and available time cards
        """
        # units
        day = datetime.timedelta(1)
        # payroll happens biweekly
        # MGA: pull this from the client configuration
        payperiod = 14*day

        # identify the time period of interest; if a specific payday were specified
        if self.payday is not None:
            # it becomes the entire range
            start = self.payday - payperiod + day
            end = self.payday
            # all done
            return start, end

        # if there is no specified payday and the user wants only the latest data
        if latest:
            # grab the payday of the last timecard
            end = timecards[-1][0]
            # back up to the first day of this period
            start = end - payperiod + day
            # all done
            return start, end

        # unpack the start of the range specified by the user
        start = self.start
        # if nothing were specified
        if start is None:
            # back up to the earliest day in the first pay period of record
            start = timecards[0][0] - payperiod + day

        # unpack the end of the range specified by the user
        end = self.end
        # if nothing were specified
        if end is None:
            # go to the last day of the last pay period on record
            end = timecards[-1][0]

        # all done
        return start, end


    # constants
    days = [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]
    TIMECARDS = r"(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})-time.csv"


# end of file
