# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis
# my superclass
from .Temporary import Temporary
# and the tables i refer to
from .Entity import Entity
from .Email import Email
from .ContactPurpose import ContactPurpose


# table declaration
class EntityEmail(Temporary, id='entity_emails'):
    """
    The email addresses of entities
    """

    # don't forget that this table derives from {Temporary}, hence it describes a relationship
    # with a potentially finite duration

    # associating an entity with an email address
    entity = praxis.db.reference(key=Entity.entity).notNull()
    email = praxis.db.reference(key=Email.email).notNull()
    # for a particular purpose
    purpose = praxis.db.reference(key=ContactPurpose.purpose).notNull()


# end of file
