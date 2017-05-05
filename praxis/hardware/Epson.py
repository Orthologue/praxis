# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


class Epson:
    """
    """


    # interface
    def selectDefaultLineSpacing(self):
        """
        Set the line spacing back to its default value; see {setDefaultLineSpacing}
        """
        # generate the sequence
        return bytes([self.ESC, ord('2')])


    def selectCharacterSize(self, width, height):
        """
        Pick the character width

        The parameters {width} and {height} are multipliers on the normal font size, in the
        range [1-8]
        """
        # normalize
        width = min(max(width-1, 0), 8) << 4
        height = min(max(height-1, 0), 8)
        # combine
        code = width + height
        # generate the sequence
        return bytes([self.GS, ord('!'), code])


    def selectJustification(self, layout):
        """
        Select the justification mode of single text

        Valid choices: "left", "center", "right"
        """
        # normalize
        layout = layout[0].lower()

        # parse
        if layout == 'c':
            code = 0x01
        elif layout == 'r':
            code = 0x02
        else:
            code = 0x00

        # generate the escape sequence
        return bytes([self.ESC, ord('a'), code])

    def feed(self, lines=None, units=None):
        """
        Print the data in the buffer and feed the indicated number of {lines}
        """
        # set up a buffer
        instructions = []
        # if the number of vertical units were specified
        if units is not None:
            # add the sequence to the instructions
            instructions.append(bytes([self.ESC, ord('J'), units]))
        # if the number of lines were specified
        if lines is not None:
            # add the sequence to the instructions
            instructions.append(bytes([self.ESC, ord('d'), lines]))

        # put it all  together
        return b''.join(instructions)


    # mechanism control commands
    def cut(self, full=True):
        """
        Set the cut type and position {units} further down
        """
        # select the cut mode
        cut = 0 if full else 1
        # generate the sequence
        return bytes([self.GS, ord('V'), 0+cut, 0])


    def feedAndCut(self, full=True, units=0):
        """
        Set the cut type and position {units} further down
        """
        # select the cut mode
        cut = 0 if full else 1
        # generate the sequence
        return bytes([self.GS, ord('V'), 65+cut, units])


    def feedCutAndFeed(self, full=True, units=0):
        """
        Set the cut type and position {units} further down
        """
        # select the cut mode
        cut = 0 if full else 1
        # generate the sequence
        return bytes([self.GS, ord('V'), 103+cut, units])


    def pulse(self, pin=2, on=2, off=2):
        """
        Send a pulse to the indicated {pin}, for the indicated time interval: {on} ms, followed
        by {off} ms
        """
        # parse the pin number
        code = 0x01 if pin == 5 else 0x00
        # generate the sequence
        return bytes([self.ESC, ord('p'), code, on//2, off//2])


    # settings
    def setCutPosition(self, full=True, units=0):
        """
        Set the cut type and position {units} further down
        """
        # select the cut mode
        cut = 0 if full else 1
        # generate the sequence
        return bytes([self.GS, ord('V'), 97+cut, units])


    def setDefaultLineSpacing(self, units):
        """
        Set line spacing
        """
        # generate the sequence
        return bytes([self.ESC, ord('3'), units])


    def setPrintMode(self, font=1,
                        emphasized=False,
                        doubleHeight=False, doubleWidth=False, underline=False):
        """
        Select the character font and style
        """
        # initialize the code
        code = 0x00
        # choose the font
        if font == 2: code |= 0x01
        # pick the emphasis mode
        if emphasized: code |= 0x08
        # pick the height
        if doubleHeight: code != 0x10
        # pick the width
        if doubleWidth: code != 0x20
        # select the underline mode
        if underline: code != 0x80

        # generate the sequence
        return bytes([self.ESC, ord('!'), code])


    def reset(self):
        """
        Reset the printer
        """
        # generate the sequence
        return bytes([self.ESC, ord('@')])

    # access to the constants
    def lf(self):
        """
        Convert into a byte
        """
        return bytes([self.LF])


    def ff(self):
        """
        Convert into a byte
        """
        return bytes([self.FF])


    def cr(self):
        """
        Convert into a byte
        """
        return bytes([self.CR])

    def esc(self):
        """
        Convert into a byte
        """
        return bytes([self.ESC])


    def fs(self):
        """
        Convert into a byte
        """
        return bytes([self.FS])


    def gs(self):
        """
        Convert into a byte
        """
        return bytes([self.GS])


    # CONSTANTS
    LF  = 0x0a
    FF  = 0x0c
    CR  = 0x0d

    CAN = 0x18
    ESC = 0x1b
    FS  = 0x1c
    GS  = 0x1d


# end of file
