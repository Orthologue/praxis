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
from .Email import Email
from .EmailType import EmailType


# table declaration
class EntityEmail(Temporary, id='entity_emails'):
    """
    The email addresses of entities
    """

    # don't forget that this table derives from {Temporary}, hence it describes a relationship
    # with a potentially finite duration

    # associating an entity with an email address
    entity = praxis.db.reference(key=Entity.eid).notNull()
    email = praxis.db.reference(key=Email.id).notNull()
    # for a particular purpose
    purpose = praxis.db.reference(key=EmailType.id).notNull()


# end of file 
