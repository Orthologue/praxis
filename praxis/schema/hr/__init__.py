# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# types
from .EmploymentType import EmploymentType as employmentType
from .PayType import PayType as payType
from .PayFrequency import PayFrequency as payFrequency

# atoms
from .Employee import Employee as employee
from .Employer import Employer as employer
# connections among atoms
from .Employment import Employment as employment


# table groups
typeTables = (
    # attribute types
    employmentType, payType, payFrequency,
)

# atoms
atomTables = (
    employee, employer,
)

# attributes
attributeTables = (
)

# relations
relationTables = (
    # connections among atoms
    employment,
)

# the table list, sorted by dependency
tables = typeTables + atomTables + attributeTables + relationTables


# end of file
