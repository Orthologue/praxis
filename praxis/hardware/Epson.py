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
    # print commands
    def lf(self):
        """
        Print and advance by a line
        """
        # generate
        return bytes([self.LF])


    def ff(self):
        """
        Page mode: print and return to standard mode
        """
        # generate
        return bytes([self.FF])


    def cr(self):
        """
        Print and carriage return
        """
        # generate
        return bytes([self.CR])


    def pageframe(self):
        """
        Page mode: print the buffered data but do not clear it or alter the print position
        """
        # generate the sequence
        return bytes([self.ESC, self.FF])


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


    # line spacing commands
    def selectDefaultLineSpacing(self):
        """
        Set the line spacing back to its default value; see {setDefaultLineSpacing}
        """
        # generate the sequence
        return bytes([self.ESC, ord('2')])


    def setDefaultLineSpacing(self, units):
        """
        Set line spacing
        """
        # generate the sequence
        return bytes([self.ESC, ord('3'), units])



    # character commands
    def can(self):
        """
        Page mode: erase the print buffer
        """
        # generate
        return bytes([self.CAN])


    def setRightSideSpacing(self, units):
        """
        Set the right side character spacing to motion {unit}s
        """
        # generate
        return bytes([self.ESC, ord(' '), units])


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


    def underline(self, thickness=0):
        """
        Turn on underline mode

        The {thickness} of the underline is specified in dots, in the range [0,2]
        """
        # generate the sequence
        return bytes([self.ESC, ord('-'), thickness])


    def emphasize(self, state=False):
        """
        Control emphasize mode
        """
        # generate the sequence
        return bytes([self.ESC, ord('E'), (1 if state else 0)])


    def doublestrike(self, state=False):
        """
        Control double-strike mode
        """
        # generate the sequence
        return bytes([self.ESC, ord('G'), (1 if state else 0)])


    def selectFont(self, font=0):
        """
        Select the character font
        """
        # generate the sequence
        return bytes([self.ESC, ord('M'), font])


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
            # center
            code = 0x01
        elif layout == 'r':
            # right justify
            code = 0x02
        else:
            # left justify
            code = 0x00

        # generate the escape sequence
        return bytes([self.ESC, ord('a'), code])


    def smoothing(self, state=True):
        """
        Turn smoothing on for large characters
        """
        # generate the escape sequence
        return bytes([self.GS, ord('b'), (1 if state else 0)])


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


    def reset(self):
        """
        Reset the printer
        """
        # generate the sequence
        return bytes([self.ESC, ord('@')])


    # access to the constants
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
