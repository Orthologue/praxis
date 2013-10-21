# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# access to the framework
import praxis
# my superclass
from .Temporary import Temporary
# and the tables i refer to
from .Entity import Entity
from .Phone import Phone
from .PhoneType import PhoneType


# table declaration
class EntityPhone(Temporary, id='entity_phones'):
    """
    The phone numbers of entities
    """

    # don't forget that this table derives from {Temporary}, hence it describes a relationship
    # with a potentially finite duration

    # associating an entity with a phone number
    entity = praxis.db.reference(key=Entity.eid).notNull()
    phone = praxis.db.reference(key=Phone.id).notNull()
    # for a particular purpose
    purpose = praxis.db.reference(key=PhoneType.id).notNull()


# end of file 
