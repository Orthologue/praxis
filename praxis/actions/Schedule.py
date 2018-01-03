#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# get the package
import praxis


# class declaration
class Schedule(praxis.command, family='praxis.actions.schedule'):
    """
    Render the staff schedule
    """


    # implementation details
    @praxis.export(tip='render the schedule as text')
    def text(self, plexus, **kwds):
        """
        Render the schedule as text
        """


    @praxis.export(tip='render the schedule as HTML')
    def html(self, plexus, **kwds):
        """
        Render the schedule as an SVG drawing embedded in an HTML page
        """


    @praxis.export(tip='render the schedule as SVG')
    def svg(self, plexus, **kwds):
        """
        Render the schedule as a stand-alone SVG drawing
        """


# end of file
