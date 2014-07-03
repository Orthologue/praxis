# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# convenient access to the command base class
from .Command import Command as command


# pull in the actions supplied by the framework
from pyre.shells.VFS import VFS as vfs


# the list of actions
def db():
    """
    Grant access to the raw database primer
    """
    # get the database primer
    from .Primer import Primer
    # and return it
    return Primer


def idd():
    """
    Grant access to the schedule manager
    """
    # get the action
    from .IDD import IDD
    # and return it
    return IDD


def schedule():
    """
    Grant access to the schedule manager
    """
    # get the action
    from .Schedule import Schedule
    # and return it
    return Schedule


def staff():
    """
    Grant access to the employee record manager
    """
    # get the action
    from .Staff import Staff
    # and return it
    return Staff


# end of file