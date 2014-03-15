#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    # get the package
    import praxis.ecrs

    # make a punch parser
    parser = praxis.ecrs.punchParser()
    # open the data stream
    with open("punches.csv") as stream:
        # and parse it
        punches = parser.parse(stream)
    # check
    print(punches)
    
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
