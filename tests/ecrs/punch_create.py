#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    # get the package
    import praxis.vendors.ecrs
    # make a punch parser
    parser = praxis.vendors.ecrs.reports.punches()
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
