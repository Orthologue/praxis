#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


"""
Parse the various test files and verify they are processed correctly
"""


# the test script
def test():
    """
    Run the various tests
    """
    # externals
    import datetime
    # get the package
    import praxis.vendors.ecrs
    # make a report parser
    parser = praxis.vendors.ecrs.reports.daily()

    # open the sample file
    with open("daily-20170416.csv", newline='') as stream:
        # and parse it
        departments, warnings, errors = parser.lastFourWeeks(stream=stream)
        # verify the payload is not empty
        assert departments

    # find the time span
    start = min(date for table in departments.values() for date in table.keys())
    end = max(date for table in departments.values() for date in table.keys())
    # an verify
    assert start == datetime.date(2017, 3, 20)
    assert end == datetime.date(2017, 4, 16)

    # we should have 16 departments in this particular file
    assert len(departments) == 16
    # print a list of the departments
    for department in sorted(departments.keys()):
        # parse the department code and name
        code, name = department.split(maxsplit=1)
        # show me
        # print(code, name.lower())

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
