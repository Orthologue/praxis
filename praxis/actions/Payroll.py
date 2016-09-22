# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import csv, datetime, re, operator
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
        # get the end of the pay period
        payday = self.payday
        # grab the folder with my data store; it's guaranteed to be there by the application
        # boot process
        etc = plexus.pfs["etc"]
        # grab the level below
        etc.discover(levels=1)
        # get the folder with the timecards
        folder = etc["timecards"].discover()

        # if the user didn't specify a payday
        if payday is None:
            # collect entries that look like timecards
            timecards = list(
                (match.group(), node)
                for node,match in folder.find(pattern=r"\d{8}-time.csv"))
            # sort them
            timecards.sort(reverse=True)
            # grab the node/path pair that corresponds to the latest one
            path, node = timecards[0]
            # now, extract the date info from the filename
            year =  int(path[0:4])
            month =  int(path[4:6])
            day =  int(path[6:8])
            # build a date object to represent the pay day
            payday = datetime.date(year=year, month=month, day=day)
        # otherwise
        else:
            # form the path of the timecard based on the payday
            path = "{0.year:04}{0.month:02}{0.day:02}-time.csv".format(payday)
            # and get the corresponding node
            node = folder[path]

        # let the user know what we are doing
        plexus.info.log('parsing clock punches from {!r}'.format(path))

        # build the employee index
        employees = {}
        # build the punch table
        punches = praxis.patterns.vivify(levels=2, atom=praxis.vendors.ecrs.model.punchlist)
        # initialize the event piles
        errors = [] # parsing errors
        warnings = [] # parsing warnings
        # make a punch parser
        parser = praxis.vendors.ecrs.punchParser()
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
        plexus.info.log('  retrieved: {} to {}'.format(datastart, dataend))

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

            # adjust for legally mandated breaks
            breaks = self.jurisdiction.breaks(start=start, workweeks=2, timecard=timecard)
            # tally them
            brkRegular, brkSesqui, brkDouble = map(sum, zip(*breaks))

            # compute the discrepancy
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


    @praxis.export(tip='classify the hours worked in a given pay period')
    def data(self, plexus, **kwds):
        """
        """
        plexus.warning.active = False
        # for date arithmetic
        day = datetime.timedelta(1)
        # get the jurisdiction
        js = self.jurisdiction
        # grab the complete data set
        timecards = self.timecards(plexus=plexus)
        # narrow the set down to the pay periods requested by the user
        dataset = self.select(timecards=timecards)
        # get the employee index and time punches
        employees, punches = self.punches(plexus=plexus, dataset=dataset)

        # activeEmployees = tuple(eid for eid in punches if len(punches[eid][self.end]) > 0)

        # build the employee name filter
        namefilter = re.compile('|'.join(name.lower() for name in self.name))
        # identify the employees of interest
        eids = tuple(
            eid
            for eid, name in employees.items()
            if namefilter.search(', '.join(name).lower()) #and eid in activeEmployees
            )

        # for each employee in the target group
        for eid in eids:
            # get the name of the employee
            last, first = employees[eid]
            # assemble the name of the output file
            name = ''.join(''.join((last, first)).split()) + '-pay.csv'
            # open it
            writer = csv.writer(open(name, 'w'))
            # leave behind the employee name
            writer.writerow(("Employee:", last, first))

            # write my heders
            writer.writerow(("Pay Period", "", "Raw", "", "Breaks", "", "Difference", ""))
            writer.writerow(("Start", "End",
                             "Regular", "Overtime", "Regular", "Overtime", "Regular", "Overtime"))

            # my accumulators
            rawRegular, rawSesqui, rawDouble = 0,0,0
            brkRegular, brkSesqui, brkDouble = 0,0,0
            # and for each available time card
            for payday in reversed(sorted(punches[eid])):
                # get the tasks
                tasks = punches[eid][payday]
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

                # save the difference
                record += ["{:.2f}".format(regularR-regularB), "{:.2f}".format(sesquiR-sesquiB)]

                # and record
                writer.writerow(record)

            # show me
            print(
                "{name:25}: {reg:6.2f} {ovr:6.2f} {dbl:6.2f}".format(
                    name = ', '.join(employees[eid]),
                    reg = rawRegular - brkRegular,
                    ovr = rawSesqui - brkSesqui,
                    dbl = rawDouble - brkDouble))

        return 0


    @praxis.export(tip='collect the clock punches of select employees')
    def record(self, plexus, **kwds):
        """
        Collect all the clock punches of select employees in separate files
        """
        # for date arithmetic
        day = datetime.timedelta(1)
        # grab the complete data set
        timecards = self.timecards(plexus=plexus)
        # narrow the set down to the pay periods requested by the user
        dataset = self.select(timecards=timecards)
        # get the employee index and time punches
        employees, punches = self.punches(plexus=plexus, dataset=dataset)

        # build the employee name filter
        namefilter = re.compile('|'.join(name.lower() for name in self.name))
        # identify the employees of interest
        eids = tuple(
            eid
            for eid, name in employees.items()
            if namefilter.search(', '.join(name).lower()) #and eid in activeEmployees
            )

        # for each employee in the target group
        for eid in eids:
            # get the name of the employee
            last, first = employees[eid]
            # assemble the name of the output file
            name = ''.join(''.join((last, first)).split()) + '-time.csv'
            # make a CSV writer
            writer = csv.writer(open(name, 'w'))
            # leave behind the employee name in the first row
            writer.writerow((last, first))

            # focus on the paydays that are relevant for this employee
            paydays = punches[eid]
            # go through them
            for payday in reversed(sorted(paydays)):
                # get the days worked during this pay period
                entries = paydays[payday]
                # and go through them in order
                for date in reversed(sorted(entries)):
                    # go through each task
                    for task in entries[date]:
                        # compute the difference and convert into hours
                        delta = (task.finish - task.start).total_seconds() / 3600
                        # write a line in the file
                        writer.writerow((date, task.start, task.finish, "{:.2f}".format(delta)))

        # all done
        return

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
        Identify the timecards of interest based on the date specification supplied
        """
        # grab the folder with my data store; it's guaranteed to be there by the application
        # boot process
        etc = plexus.pfs["etc"]
        # grab the level below
        etc.discover(levels=1)
        # get the folder with the timecards
        folder = etc["timecards"].discover()
        # collect all entries that look like timecards
        timecards = [
            (datetime.date(year = int(match.group('year')),
                           month = int(match.group('month')),
                           day = int(match.group('day'))),
             node)
            for node,match in folder.find(pattern=self.TIMECARDS)]
        # sort them
        timecards.sort()
        # and return them
        return timecards


    def select(self, timecards):
        """
        Identify the timecards that are consistent with the period specified by the user
        """
        # units
        day = datetime.timedelta(1)
        # adjust the interval endpoints
        # N.B.: the logic below assumes that {timecards} is sorted by date
        # if no starting point has been specified
        if self.start is None:
            # backup to the first day of the first pay period
            self.start = timecards[0][0] - 13*day
        # similarly, if no end date has been specified
        if self.end is None:
            # adjust it to the last day of the last pay period
            self.end = timecards[-1][0]

        # payroll is biweekly
        fourteen = 14*day
        # my filter
        def choose(entry, start=self.start, end=self.end, duration=fourteen):
            """
            Pick timecards whose dates that are no earlier than {start} and no later than {end}
            """
            # unpack
            stamp = entry[0]
            # if it's in the interval
            if (stamp >= start) and (stamp-end < duration):
                # all good
                return True
            # otherwise reject it
            return False

        # go through the timecards and filter them
        selection = tuple(filter(choose, timecards))
        # adjust my time range one last time
        self.start = selection[0][0] - 13*day
        self.end = selection[-1][0]
        # and return the selected datasets
        return selection



    def punches(self, plexus, dataset):
        """
        Load the clock punches from the sequence of {date, vnode} pairs
        """
        # build the employee index
        employees = {}
        # and the punch data
        index = praxis.patterns.vivify(levels=3, atom=praxis.vendors.ecrs.model.punchlist)
        # initialize the event piles
        errors = [] # parsing errors
        warnings = [] # parsing warnings
        # make a punch parser
        parser = praxis.vendors.ecrs.punchParser()

        # go through the timecard specs
        for payperiod, node in dataset:
            # build the punch table
            punches = praxis.patterns.vivify(levels=2, atom=praxis.vendors.ecrs.model.punchlist)
            # open the file
            with node.open() as stream:
                # parse
                parser.parse(stream = stream, names = employees, punches = punches,
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

        # return the employee index and time punches
        return employees, index


    # constants
    days = [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]
    TIMECARDS = r"(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})-time.csv"


# end of file
