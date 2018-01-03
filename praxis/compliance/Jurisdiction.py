# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# get the package
import pyre


# class declaration
class Jurisdiction(pyre.protocol, family="praxis.compliance"):
    """
    Protocol declaration for all compliance components
    """


    # interface
    @pyre.provides
    def overtime(self, start, workweeks, timecard):
        """
        Classify the hours worked by an employee a given an employee's time card
        """


    @pyre.provides
    def breaks(self, timecard):
        """
        Same as {overtime} except the calculator enforces the legally mandated breaks
        """


# end of file
