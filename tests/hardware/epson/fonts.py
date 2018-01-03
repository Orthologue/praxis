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
        p.setDefaultLineSpacing(18),

        # select font A
        p.selectFont(font=0),
        # 1x1
        p.selectCharacterSize(height=1, width=1),
        b'Urban Radish\n',
        # 2x1
        p.selectCharacterSize(height=2, width=1),
        b'Urban Radish\n',
        # 2x2
        p.selectCharacterSize(height=2, width=2),
        b'Urban Radish\n',
        # 3x1
        p.selectCharacterSize(height=3, width=1),
        b'Urban Radish\n',
        # 3x2
        p.selectCharacterSize(height=3, width=2),
        b'Urban Radish\n',
        # 3x3
        p.selectCharacterSize(height=3, width=3),
        b'Urban Radish\n',

        # select font b
        p.selectFont(font=1),
        # 1x1
        # 1x1
        p.selectCharacterSize(height=1, width=1),
        b'Urban Radish\n',
        # 2x1
        p.selectCharacterSize(height=2, width=1),
        b'Urban Radish\n',
        # 2x2
        p.selectCharacterSize(height=2, width=2),
        b'Urban Radish\n',
        # 3x1
        p.selectCharacterSize(height=3, width=1),
        b'Urban Radish\n',
        # 3x2
        p.selectCharacterSize(height=3, width=2),
        b'Urban Radish\n',
        # 3x3
        p.selectCharacterSize(height=3, width=3),
        b'Urban Radish\n',

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
