#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to my superclass
import pyre.parsing


# class declaration
class ScheduleScanner(pyre.parsing.scanner):
    """
    Convert a schedule specification into a stream of tokens
    """

    # the tokens
    employee = pyre.parsing.token(
        head = '\[\s*', pattern='\w+\s\w+', tail='\s*\]')

    days = pyre.parsing.token(
        pattern = r'((\s*,\s*)|monday|tuesday|wednesday|thursday|friday|saturday|sunday)+',
        tail = '\s*:')

    task = pyre.parsing.token(
        pattern = '(?P<station>[a-z-_.]+)\s@\s(?P<time>\d{1,2}:\d{2}(a|p)m)')

    comment = pyre.parsing.token(head=';', pattern=r'.*', tail='$')
    

    # interface
    def pyre_tokenize(self, uri, stream, client):
        """
        Convert the input {stream} into tokens; absorb whitespace
        """
        # adjust the client
        filtered = self.pyre_ignoreWhitespace(client)
        # and process the token stream
        return super().pyre_tokenize(uri=uri, stream=stream, client=filtered)


# end of file 
