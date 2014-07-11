#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# urban radish
# (c) 2011-2014 all rights reserved
#


# get the package
import praxis


# class declaration
class Schedule(praxis.command, family='praxis.actions.schedule'):
    """
    Render a schedule
    """


    # command obligations
    @praxis.export
    def help(self, plexus, **kwds ):
        """
        Show a help screen
        """
        # here is the list of my commands
        commands = ' | '.join(['text', 'html', 'svg'])
        # show me
        self.info.line(
            '{.pyre_spec}: a family of tools for managing employee scheduling'.format(self))
        self.info.line('usage: {.pyre_namespace} {.pyre_spec} [{}]'.format(plexus, self, commands))
        self.info.log()
        # all done
        return 0


    # implementation details
    def text(self, plexus, **kwds):
        """
        Render the schedule as text
        """


    def html(self, plexus, **kwds):
        """
        Render the schedule as an SVG drawing embedded in an HTML page
        """


    def svg(self, plexus, **kwds):
        """
        Render the schedule as a stand-alone SVG drawing
        """


# end of file 
