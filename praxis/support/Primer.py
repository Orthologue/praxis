# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


class Primer:
    """
    Populate a freshly instantiated schema with canonical data
    """


    # interface
    def prime(self, tokenGenerator, datastore, **kwds):
        """
        Main entry point that delegates table priming to the more specialized hooks
        """
        # get access to the schema
        schema = datastore.schema

        # walk through the chain of tables
        yield from self.primeEntityTypes(tokenGenerator, schema, **kwds)
        yield from self.primeItemTypes(tokenGenerator, schema, **kwds)
        yield from self.primeContactTypes(tokenGenerator, schema, **kwds)
        yield from self.primeLocationTypes(tokenGenerator, schema, **kwds)
        yield from self.primeEmailTypes(tokenGenerator, schema, **kwds)
        yield from self.primePhoneTypes(tokenGenerator, schema, **kwds)
        yield from self.primeURITypes(tokenGenerator, schema, **kwds)
        yield from self.primePayTypes(tokenGenerator, schema, **kwds)

        # all done
        return


    # implementation details
    def primeEntityTypes(self, tokenGenerator, schema, **kwds):
        """
        Create the default entity types
        """
        # get the entity type factory
        factory = schema.entityType
        # the built-in entity types
        names = [ "companies", "persons" ]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=tokenGenerator(), description=name)
        # all  done
        return


    def primeItemTypes(self, tokenGenerator, schema, **kwds):
        """
        Create the default item types
        """
        # get the item type factory
        factory = schema.itemType
        # the built-in item types
        names = ["products", "services"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=tokenGenerator(), description=name)
        # all  done
        return


    def primeContactTypes(self, tokenGenerator, schema, **kwds):
        """
        Create the default contact types
        """
        # get the contact type factory
        factory = schema.contactType
        # build the records; the values are supposed to match names of tables in the current
        # schema that contain contact information
        names = ["email", "location", "phone", "uri"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=tokenGenerator(), description=name)
        # all  done
        return


    def primeLocationTypes(self, tokenGenerator, schema, **kwds):
        """
        Create the default location types
        """
        # get the location type factory
        factory = schema.locationType
        # the built-in location types
        names = ["home", "office", "shipping", "billing" ]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=tokenGenerator(), description=name)
        # all  done
        return


    def primeEmailTypes(self, tokenGenerator, schema, **kwds):
        """
        Create the default email types
        """
        # get the email type factory
        factory = schema.emailType
        # the built-in email types
        names = ["home", "work" ]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=tokenGenerator(), description=name)
        # all  done
        return


    def primePhoneTypes(self, tokenGenerator, schema, **kwds):
        """
        Create the default phone types
        """
        # get the phone type factory
        factory = schema.phoneType
        # the built-in phone types
        names = ["cell", "fax", "land line" ]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=tokenGenerator(), description=name)
        # all  done
        return


    def primeURITypes(self, tokenGenerator, schema, **kwds):
        """
        Create the default uri types
        """
        # get the uri type factory
        factory = schema.uriType
        # the built-in uri types
        names = ["web", "facebook", "instagram", "twitter", "vine", "youtube"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=tokenGenerator(), description=name)
        # all  done
        return


    def primePayTypes(self, tokenGenerator, schema, **kwds):
        """
        Create the default pay types
        """
        # get the pay type factory
        factory = schema.payType
        # the built-in pay types
        names = ["hourly", "salary"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=tokenGenerator(), description=name)
        # all  done
        return


# end of file
