#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


"""
Parse the various test files and verify they are processed correctly
"""


# the test script
def test():
    """
    Run the various tests
    """
    # journal
    import journal
    error = journal.error("praxis.ecrs")
    warning = journal.warning("praxis.ecrs")
    # get the package
    import praxis.vendors.ecrs
    # make a punch parser
    parser = praxis.vendors.ecrs.reports.punches()

    # the empty file
    with open("punches-empty.csv") as stream:
        # and parse it
        names, punches, warnings, errors = parser.parse(stream=stream)
        # verify the payload is empty
        assert not names
        assert not punches
        assert not warnings
        assert not errors

    # a complete cycle
    with open("punches-inout.csv") as stream:
        # an employee id that is known to exist in this file
        eid = '1000'
        # parse it
        names, punches, warnings, errors = parser.parse(stream=stream)
        # compute the hours: it is a double sum over the hours worked in a given day and over
        # the days in the data set
        total = sum(card.hours for card in punches[eid].values())
        # verify the payload is correct
        assert total == 8
        # nothing should have gone wrong
        assert not warnings
        assert not errors

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
