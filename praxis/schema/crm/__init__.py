# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# get the db support
from .. import db


# literals, for convenience
null = db.null
default = db.default


# types
from .ContactPurpose import ContactPurpose as contactPurpose
from .ContactType import ContactType as contactType
from .EntityType import EntityType as entityType
from .PhoneType import PhoneType as phoneType
from .URIType import URIType as uriType

# atoms
from .Entity import Entity as entity
from .Company import Company as company
from .Person import Person as person
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


# table groups
# types
typeTables = (
    # attribute types
    entityType,
    contactPurpose, contactType, phoneType, uriType,
)

# atoms
atomTables = (
    entity, company, person,
)

# attributes
attributeTables = (
    email, location, phone, uri,
)

# relations
relationTables = (
    # connections between atoms and their attributes
    entityEmail, entityLocation, entityPhone, entityURI,
)

# the table list, sorted by dependency
tables = typeTables + atomTables + attributeTables + relationTables


# end of file
