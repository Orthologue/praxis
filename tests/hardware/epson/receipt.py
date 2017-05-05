#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


"""
The 'receipt' programming example from the EPSON distribution
"""


def test():
    # access
    import praxis.hardware
    # make an instance
    p = praxis.hardware.epson()
    # build a document
    doc = [
        # set up
        p.reset(),
        p.setDefaultLineSpacing(18),
        p.selectJustification(layout='center'),
        p.selectCharacterSize(width=2, height=4),

        # EPSON logo in a box
        b'\xc9' + b'\xcd'*11 + b'\xbb' + p.lf(),
        b'\xba\x20\x20\x20\x45\x50\x53\x4F\x4e\x20\x20\x20\xba' + p.lf(),
        b'\xba\x20\x20\x20',
        p.selectCharacterSize(width=1, height=1),
        b'Thank you ',
        p.selectCharacterSize(width=2, height=4),
        b'\x20\x20\x20\xba' + p.lf(),
        b'\xc8' + b'\xcd'*11 + b'\xbc' + p.lf(),

        # go back to defaults
        p.selectDefaultLineSpacing(),
        p.selectCharacterSize(1,1),

        # print date and time
        p.feed(units=4),
        b'November 1, 2012  10:30',
        p.feed(lines=3),

        # print the receipt details A
        p.selectJustification(layout='left'),
        b'TM-Uxxx                            6.75' + p.lf(),
        b'TM-Hxxx                            6.00' + p.lf(),
        b'PS-Hxxx                            1.70' + p.lf() + p.lf(),

        # print the receipt details B
        p.selectCharacterSize(width=1,height=2),
        b'TOTAL                             14.45' + p.lf(),
        p.selectCharacterSize(width=1,height=1),
        b'---------------------------------------' + p.lf(),
        b'PAID                              50.00' + p.lf(),
        b'CHANGE                            35.55' + p.lf(),

        # open the drawer
        p.pulse(pin=2, on=4, off=400),

        # select cut mode and cut the paper
        p.feedAndCut(full=False),
        ]
    # open a file
    stream = open("receipt.eps", "wb")
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
