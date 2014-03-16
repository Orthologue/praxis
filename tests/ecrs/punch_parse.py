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
        data = parser.parse(stream)
    # check
    for id in sorted(data):
        # pull the activity for this employee
        punches = data[id]
        # zero out the number of hours worked
        hours = 0
        # go through all the punches
        for clockin, clockout in punches:
            # if there is no clockout, there's nothing to do
            if not clockout: continue
            # otherwise, subtract the two timestamps
            delta = clockout - clockin
            # adjust the hours worked
            hours += 24*delta.days + delta.seconds/3600
        # show me
        print("{}: {:5.2f}".format(id, hours))
    
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
