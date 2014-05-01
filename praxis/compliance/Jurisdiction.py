# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
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
    def overtime(self, timecard):
        """
        Classify the hours worked by an employee a given an employee's time card
        """


# end of file 
