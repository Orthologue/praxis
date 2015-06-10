# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import re
# get the package
import praxis


# the action
class Payroll(praxis.command, family='praxis.actions.payroll'):
    """
    Payroll support
    """


    # public state
    payday = praxis.properties.date(default='20150531', format='%Y%m%d')
    payday.doc = 'the pay period to process'

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
    @praxis.export(tip='parse an ECRS timecard to get hours worked')
    def hours(self, plexus):
        """
        Run payroll for a given pay period
        """
        # get the end of the pay period
        payday = self.payday
        # build the employee index
        employees = {}
        # build the punch table
        punches = praxis.patterns.vivify(levels=2, atom=praxis.model.punchlist)
        # make a punch parser
        parser = praxis.vendors.ecrs.punchParser()
        # form the name of the timecard based on the payday
        timecard = "/etc/timecards/{0.year:04}{0.month:02}{0.day:02}-time.csv".format(payday)
        # let the user know what we are doing
        plexus.info.log('parsing clock punches from {!r}'.format(timecard))
        # open the timecards
        with plexus.pfs[timecard].open() as stream:
            # parse the input stream
            parser.parse(
                stream=stream, errorlog=plexus.error, warninglog=plexus.warning,
                names=employees, punches=punches
        )

        # get the {datetime} package
        import datetime
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

        # get {operator} so we can sort the employees by name
        import operator
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
