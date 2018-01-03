# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# externals
import csv, datetime


# declaration
class EarningsRecord:
    """
    A parser of the ADP employment records report that contains paystub summary information.
    """


    # interface
    def parse(self, employees, records, stream):
        """
        Extract employee earning records from {stream} and populate {records}
        """
        # make a CSV reader from {stream}
        reader = csv.reader(stream)
        # skip the first three lines
        next(reader)
        next(reader)
        next(reader)
        # the next line is the first employee record
        line = next(reader)
        # start parsing
        while line:
            # get the zeroth field
            header = line[0]
            # check that it is an employee section
            assert header.startswith('Employee: ')
            # extract the useful info
            name = header[9:].strip()
            # pull the employee record
            line = self.getEmployeeRecord(
                employees=employees, records=records, name=name, reader=reader)

        # all done
        return


    # implementation details
    def getEmployeeRecord(self, employees, records, name, reader):
        """
        Extract the paychecks for a given employee
        """
        # pull the first and last name of the employee
        last, first = name.split(',')
        # clean up, if necessary
        last = last.strip()
        first = first.split()[0].strip()
        # get the next line with the social security number
        text = next(reader)[0]
        # check that it is the right line
        assert text.startswith('SSN: ')
        # extract the obfuscated number
        ssn = text[5:].strip().replace('x', '?')

        # go through the employee index looking for a name match
        for eid, fullname in employees.items():
            # if this is the match
            if fullname == (last, first):
                # bail
                break
        # if we get this far, there is no match
        else:
            # complain
            # print('could not match {} {}'.format(first, last))
            # make one up
            eid = ((last, first), ssn)

        # attempt to
        try:
            # look up the employee
            employee = records[eid]
        # if that fails
        except KeyError:
            # build the employee record
            employee = Employee(first=first, last=last, ssn=ssn)
            # and attach it
            records[eid] = employee

        # grab the next line
        line = next(reader)
        # start parsing paycheck info
        while line:
            # have we reached the summary section?
            if line[0].startswith('Employee Totals:'):
                # swallow this section
                for line in reader:
                    # bail if the zeroth field isn't empty; it's the end of the section
                    if line[0]: return line
                # ran out of input
                break
            # otherwise, this is a paycheck section; extract
            line = self.getEmployeePaycheck(employee=employee, header=line, reader=reader)

        # if we get this far, the input was exhausted and we are all done
        return


    def getEmployeePaycheck(self, employee, header, reader):
        """
        Extract a single paycheck
        """
        # extract the paycheck date and normalize it
        date = datetime.datetime.strptime(header[0], '%m/%d/%y').date()
        # make a paycheck
        paycheck = Paycheck(date=date)
        # save it
        employee.paychecks[paycheck.date] = paycheck

        # the gross pay
        paycheck.gross = float(header[5].strip())
        # the net pay
        paycheck.net = float(header[12].strip())

        # extract the paycheck info
        self.getIncomeAndDeductions(paycheck=paycheck, record=header)
        # process the remaining lines
        for record in reader:
            # if the zeroth field isn't empty
            if record[0]:
                # we are done with this paycheck
                return record
            # otherwise, get more
            self.getIncomeAndDeductions(paycheck=paycheck, record=record)

        # all done
        return


    def getIncomeAndDeductions(self, paycheck, record):
        """
        Extract paycheck info from {text}
        """
        # the income category
        source = record[1].strip()
        # if it is not blank
        if source:
            # the pay rate for this category
            rate = record[2].strip()
            rate = float(rate) if rate else 0
            # the hours worked in this category
            hours = record[3].strip()
            hours = float(hours) if hours else 80
            # the amount earned
            amount = (record[4].strip())
            amount = float(amount) if amount else 0

            # adjust the hours earned by the salaried people
            if hours == 0 and amount > 0: hours = 80

            # make an income record
            income = Income(
                category = source.lower(),
                amount = amount,
                rate = rate, hours = hours,
                salary = 0 if rate else amount
                )
            # record
            paycheck.source[income.category] = income

        # the federal deductions
        source = record[6].strip()
        # if there
        if source:
            # get the amount
            amount = float(record[7].strip())
            # record
            paycheck.federal[source] = amount

        # the state deductions
        source = record[8].strip()
        # if there
        if source:
            # get the amount
            amount = float(record[9].strip())
            # record
            paycheck.state[source] = amount

        # the personal deductions
        source = record[10].strip()
        # if there
        if source:
            # get the amount
            amount = float(record[11].strip())
            # record
            paycheck.personal[source] = amount

        # all done
        return


class Employee:
    """
    Encapsulation of employee records
    """

    # public data
    first = ''
    last = ''
    ssn = ''
    paychecks = None

    @property
    def name(self):
        """
        Construct the employee's full name
        """
        # easy enough
        return "{0.first} {0.last}".format(self)


    # meta-methods
    def __init__(self, first, last, ssn, **kwds):
        # chain up
        super().__init__(**kwds)
        # save
        self.first = first
        self.last = last
        self.ssn = ssn
        # initialize
        self.paychecks = {}
        # all done
        return


    def __str__(self):
        return "{0.name} ({0.ssn})".format(self)


class Paycheck:
    """
    Encapsulation of the information on a single paycheck
    """

    # public data
    date = None
    source = None
    federal = None
    state = None
    personal = None
    gross = 0
    net = 0

    # meta-methods
    def __init__(self, date, **kwds):
        # chain up
        super().__init__(**kwds)
        # convert and save the date
        self.date = date
        # prime the income
        self.source = {}
        # initialize the deductions
        self.federal = {}
        self.state = {}
        self.personal = {}
        # and the pay
        self.net = 0
        self.gross = 0
        # all done
        return


class Income:
    """
    Encapsulation of the pay details
    """

    # public data
    hours = 0
    rate = 0
    salary = 0
    amount = 0
    category = ""

    # meta-methods
    def __init__(self, category="regular", amount=0, salary=0, rate=0, hours=80, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the state
        self.category = category
        self.amount = amount
        self.rate = rate
        self.hours = hours
        self.salary = salary
        # all done
        return



# end of file
