#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    # get {praxis}
    import praxis

    # create a calculator compliant with California laws and regulations
    california = praxis.compliance.us.california()

    # four twelve-hour days
    hours = (12, 12, 12, 12, 0, 0, 0)
    # compute the hour tiers
    tiers = california._overtime(hours=hours)
    # check
    assert tiers == (32, 16, 0)

    # three ten-hour days
    hours = (10, 10, 10, 0, 0, 0, 0)
    # compute the hour tiers
    tiers = california._overtime(hours=hours)
    # check
    assert tiers == (24, 6, 0)

    # six eight-hour days
    hours = (8, 8, 8, 8, 8, 8, 0)
    # compute the hour tiers
    tiers = california._overtime(hours=hours)
    # check
    assert tiers == (40, 8, 0)

    # six eleven-hour days
    hours = (11, 11, 11, 11, 11, 11, 0)
    # compute the hour tiers
    tiers = california._overtime(hours=hours)
    # check
    assert tiers == (40, 26, 0)

    # four eleven-hour days
    hours = (11, 11, 11, 11, 0, 0, 0)
    # compute the hour tiers
    tiers = california._overtime(hours=hours)
    # check
    assert tiers == (32, 12, 0)

    # overworked
    hours = (11, 15, 14, 9, 8, 14, 10)
    # compute the hour tiers
    tiers = california._overtime(hours=hours)
    # check
    assert tiers == (40, 32, 9)

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
