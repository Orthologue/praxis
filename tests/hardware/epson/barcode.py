#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


"""
The 'barcode' programming example from the EPSON distribution
"""


def test():
    # access
    import praxis
    # make an instance
    p = praxis.hardware.epson()

    # build a document
    doc = [
        # set up
        p.reset(),
        # select cut mode and cut the paper
        p.feedAndCut(full=False),
        ]

    # build the output file name out of this one
    name = praxis.primitives.path(__file__).stem + '.eps'
    # open a file
    stream = open(name, "wb")
    # render
    stream.write(b''.join(doc))
    # flush
    stream.close()

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
