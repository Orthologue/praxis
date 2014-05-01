#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Parse the various test files and verify they are processed correctly
"""


# the test script
def test():
    """
    Run the various tests
    """
    # get the package
    import praxis.ecrs
    # make a punch parser
    parser = praxis.ecrs.punchParser()

    # the empty file
    with open("punches-empty.csv") as stream:
        # and parse it
        names, punches = parser.parse(stream)
        # verify the payload is empty
        assert not names
        assert not punches

    # a complete cycle
    with open("punches-inout.csv") as stream:
        # an employee id that is know to exist in this file
        eid = '1000'
        # parse it
        names, punches = parser.parse(stream)
        # compute the hours: it is a double sum over the hours worked in a given day and over
        # the days in the data set
        total = sum(sum(card.hours()) for card in punches[eid].values())
        # verify the payload is correct
        assert total == 8

    # all done
    return


# the workhorse
def computeHours(data):
    # build the table of hours
    table = {}
    # check
    for id in sorted(data):
        # pull the activity for this employee
        punches = data[id]
        # zero out the number of hours worked
        hours = 0
        # go through all the punches
        for clockin, clockout in punches:
            # if there is no clockin or clockout, there's nothing to do
            if not (clockin and clockout): continue
            # otherwise, subtract the two timestamps
            delta = clockout - clockin
            # adjust the hours worked
            hours += 24*delta.days + delta.seconds/3600
        # save the calculated hours
        table[id] = hours
    
    # all done
    return table


# main
if __name__ == "__main__":
    test()


# end of file
