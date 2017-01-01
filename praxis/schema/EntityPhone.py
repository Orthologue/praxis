# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# access to the framework
import praxis
# my superclass
from .Temporary import Temporary
# and the tables i refer to
from .Entity import Entity
from .Phone import Phone
from .PhoneType import PhoneType
from .ContactPurpose import ContactPurpose


# table declaration
class EntityPhone(Temporary, id='entity_phones'):
    """
    The phone numbers of entities
    """

    # don't forget that this table derives from {Temporary}, hence it describes a relationship
    # with a potentially finite duration

    # associating an entity
    entity = praxis.db.reference(key=Entity.entity).notNull()
    # with a phone number
    phone = praxis.db.reference(key=Phone.number).notNull()
    # of a particular type
    type = praxis.db.reference(key=PhoneType.type).notNull()
    # for a particular purpose
    purpose = praxis.db.reference(key=ContactPurpose.purpose).notNull()


# end of file
