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
    # journal
    import journal
    error = journal.error("praxis.ecrs")
    warning = journal.warning("praxis.ecrs")
    # get the package
    import praxis.vendors.ecrs
    # make a punch parser
    parser = praxis.vendors.ecrs.reports.staff()

    # the empty file
    with open("staff-20161026.csv") as stream:
        # and parse it
        names, warnings, errors = parser.parse(stream=stream)
        # verify the payload is empty
        assert not names

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
