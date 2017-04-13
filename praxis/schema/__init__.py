# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# get the db support
from .. import db


# literals, for convenience
null = db.null
default = db.default


# types
from .ContactPurpose import ContactPurpose as contactPurpose
from .ContactType import ContactType as contactType
from .EmploymentType import EmploymentType as employmentType
from .EntityType import EntityType as entityType
from .ItemType import ItemType as itemType
from .PayType import PayType as payType
from .PayFrequency import PayFrequency as payFrequency
from .PhoneType import PhoneType as phoneType
from .TenderType import TenderType as tenderType
from .URIType import URIType as uriType

# atoms
from .Entity import Entity as entity
from .Company import Company as company
from .Item import Item as item
from .Person import Person as person
from .Employee import Employee as employee
from .Employer import Employer as employer
# attributes
from .Email import Email as email
from .Location import Location as location
from .Phone import Phone as phone
from .URI import URI as uri
# connections between atoms and their attributes
from .EntityEmail import EntityEmail as entityEmail
from .EntityLocation import EntityLocation as entityLocation
from .EntityPhone import EntityPhone as entityPhone
from .EntityURI import EntityURI as entityURI
# connections among atoms
from .Employment import Employment as employment


# table groups
typeTables = (
    # attribute types
    entityType, itemType,
    contactPurpose, contactType, phoneType, tenderType, uriType,
    employmentType, payType, payFrequency,
)

# the table list, sorted by dependency
tables = typeTables + (
    # atoms
    entity, company, item, person, employee, employer,
    # attributes
    email, location, phone, uri,
    # connections between atoms and their attributes
    entityEmail, entityLocation, entityPhone, entityURI,
    # connections among atoms
    employment
)


# end of file
