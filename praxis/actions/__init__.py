# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# get the action markers
from .. import action, foundry


# the list of actions
@foundry(implements=action, tip="access the raw database primer")
def db():
    """
    Grant access to the raw database primer
    """
    # get the database primer
    from .Primer import Primer
    # and return it
    return Primer


def debug(implements=action, tip="debugging/development support"):
    """
    Debug support
    """
    # get the action
    from .Debug import Debug
    # and return it
    return Debug


@foundry(implements=action, tip="access the token generator")
def idd():
    """
    Grant access to the token generator
    """
    # get the action
    from .IDD import IDD
    # and return it
    return IDD


@foundry(implements=action, tip="access the payroll manager")
def payroll():
    """
    Grant access to the payroll manager
    """
    # get the action
    from .Payroll import Payroll
    # and return it
    return Payroll


@foundry(implements=action, tip="access to the ECRS transaction journal")
def tj():
    """
    Analyze the transaction journal
    """
    # get the action
    from .Transactions import Transactions
    # and return it
    return Transactions


@foundry(implements=action, tip="access the schedule manager")
def schedule():
    """
    Grant access to the schedule manager
    """
    # get the action
    from .Schedule import Schedule
    # and return it
    return Schedule


@foundry(implements=action, tip="access the employee record manager")
def staff():
    """
    Grant access to the employee record manager
    """
    # get the action
    from .Staff import Staff
    # and return it
    return Staff


# administrivia
@foundry(implements=action, tip="display information about this application")
def about():
    """
    Display information about this application
    """
    from .About import About
    return About


# end of file
