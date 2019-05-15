#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


"""
Sanity check: verify that support for the EPSON printer is accessible
"""


def test():
    # access
    import praxis
    # instantiate
    praxis.hardware.epson()
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
