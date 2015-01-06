# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# get the action markers
from .. import action, foundry
# convenient access to the command base class
from .Command import Command as command


# pull in the actions supplied by the framework
from pyre.shells.VFS import VFS as vfs


# the list of actions
@foundry(implements=action)
def db():
    """
    Grant access to the raw database primer
    """
    # get the database primer
    from .Primer import Primer
    # and return it
    return Primer


@foundry(implements=action)
def debug():
    """
    Debug support
    """
    # get the action
    from .Debug import Debug
    # and return it
    return Debug


@foundry(implements=action)
def idd():
    """
    Grant access to the schedule manager
    """
    # get the action
    from .IDD import IDD
    # and return it
    return IDD


@foundry(implements=action)
def schedule():
    """
    Grant access to the schedule manager
    """
    # get the action
    from .Schedule import Schedule
    # and return it
    return Schedule


@foundry(implements=action)
def staff():
    """
    Grant access to the employee record manager
    """
    # get the action
    from .Staff import Staff
    # and return it
    return Staff


# administrivia
@foundry(implements=action)
def copyright():
    from .Copyright import Copyright
    return Copyright

@foundry(implements=action)
def license():
    from .License import License
    return License

@foundry(implements=action)
def version():
    from .Version import Version
    return Version


# end of file
