# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# get the db support
from .. import db


# literals, for convenience
null = db.null
default = db.default


# types
from .EmailType import EmailType as emailType
from .EntityType import EntityType as entityType
from .ItemType import ItemType as itemType
from .LocationType import LocationType as locationType
from .PayType import PayType as payType
from .PayFrequency import PayFrequency as payFrequency
from .PhoneType import PhoneType as phoneType
from .URIType import URIType as uriType

# atoms
from .Entity import Entity as entity
from .Company import Company as company
from .Item import Item as item
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
# connections among atoms
from .Employment import Employment as employment


# the table list, sorted by dependency
tables = (
    # contact management
    # attribute types
    emailType, entityType, itemType, locationType, payType, payFrequency, phoneType, uriType,
    # atoms
    entity, company, item, person,
    # attributes
    email, location, phone, uri,
    # connections between atoms and their attributes
    entityEmail, entityLocation, entityPhone, entityURI,
    # connections among atoms
    employment
)


# end of file 
