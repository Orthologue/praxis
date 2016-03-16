# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import re, operator, datetime
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

    name = praxis.properties.strings(default='.*')
    name.doc = 'show only information relevant for employees whose names match this regex'

    details = praxis.properties.bool(default=False)
    details.doc = 'controls whether to show the punch clock details'

    daily = praxis.properties.bool(default=False)
    daily.doc = 'controls whether to show daily summary'

    breaks = praxis.properties.bool(default=True)
    breaks.doc = 'enforce the legally mandated breaks'

    jurisdiction = praxis.compliance.jurisdiction(default='us.california')
    jurisdiction.doc = 'compliant calculators for the company jurisdiction'


    # behaviors
    @praxis.export(tip='classify the hours worked in a given pay period')
    def hours(self, plexus):
        """
        Parse ECRS timecards for the pay period specified by the given payday
        """
        # get the end of the pay period
        payday = self.payday
        # get the folder with the timecards
        folder = plexus.pfs["/etc/timecards"]

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
        punches = praxis.patterns.vivify(levels=2, atom=praxis.model.punchlist)
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

            # adjust for legally mandated breaks
            breaks = self.jurisdiction.breaks(start=start, workweeks=2, timecard=timecard)
            # tally them
            regular, sesqui, double = map(sum, zip(*breaks))
            # show me
            print("{:25}: {:6.2f} {:6.2f} {:6.2f}".format(fullname, regular, sesqui, double))
            # if we are not enforcing the legally mandated breaks
            if not self.breaks:
                # classify the hours worked
                hours = self.jurisdiction.overtime(start=start, workweeks=2, timecard=timecard)
                # tally them
                regular, sesqui, double = map(sum, zip(*hours))
                # show me
                print("{:25}: {:6.2f} {:6.2f} {:6.2f}".format('', regular, sesqui, double))

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


    # implementation details
    def payperiod(self, data):
        """
        Compute the time span over which we are tabulating hours worked
        """
        # create a set of all punch dates by all employees
        dates = { date for punches in data.values() for date in punches }
        return min(dates), max(dates)


    # constants
    days = [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]


# end of file
