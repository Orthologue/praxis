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
    def prime(self, tokenGenerator, schema, records=None, **kwds):
        """
        Main entry point that delegates table priming to the more specialized hooks
        """
        # build the list of records we will add to the database
        records = records if records is not None else []

        # walk through the chain of tables
        self.primeEntityTypes(tokenGenerator, schema, records, **kwds)
        self.primeItemTypes(tokenGenerator, schema, records, **kwds)
        self.primeContactTypes(tokenGenerator, schema, records, **kwds)
        self.primeLocationTypes(tokenGenerator, schema, records, **kwds)
        self.primeEmailTypes(tokenGenerator, schema, records, **kwds)
        self.primePhoneTypes(tokenGenerator, schema, records, **kwds)
        self.primeURITypes(tokenGenerator, schema, records, **kwds)
        self.primePayTypes(tokenGenerator, schema, records, **kwds)

        # all done
        return records


    # implementation details
    def primeEntityTypes(self, tokenGenerator, schema, records, **kwds):
        """
        Create the default entity types
        """
        # pull the entity types
        entities = schema.entityType
        # add to the list of records
        records += [
            entities.pyre_immutable(id=tokenGenerator(), description="companies"),
            entities.pyre_immutable(id=tokenGenerator(), description="persons"),
            ]
        # all  done
        return


    def primeItemTypes(self, tokenGenerator, schema, records, **kwds):
        """
        Create the default item types
        """
        # pull the item types
        items = schema.itemType
        # add to the list of records
        records += [
            items.pyre_immutable(id=tokenGenerator(), description="products"),
            items.pyre_immutable(id=tokenGenerator(), description="services"),
            ]
        # all  done
        return


    def primeContactTypes(self, tokenGenerator, schema, records, **kwds):
        """
        Create the default contact types
        """
        # pull the contact types
        contacts = schema.contactType
        # add to the list of records; the values are supposed to match names of tables in
        # the current schema that contain contact information
        records += [
            contacts.pyre_immutable(id=tokenGenerator(), description="email"),
            contacts.pyre_immutable(id=tokenGenerator(), description="location"),
            contacts.pyre_immutable(id=tokenGenerator(), description="phone"),
            contacts.pyre_immutable(id=tokenGenerator(), description="uri"),
            ]
        # all  done
        return


    def primeLocationTypes(self, tokenGenerator, schema, records, **kwds):
        """
        Create the default location types
        """
        # pull the location types
        locations = schema.locationType
        # add to the list of records
        records += [
            locations.pyre_immutable(id=tokenGenerator(), description="home"),
            locations.pyre_immutable(id=tokenGenerator(), description="office"),
            locations.pyre_immutable(id=tokenGenerator(), description="shipping"),
            locations.pyre_immutable(id=tokenGenerator(), description="billing"),
            ]
        # all  done
        return


    def primeEmailTypes(self, tokenGenerator, schema, records, **kwds):
        """
        Create the default email types
        """
        # pull the email types
        emails = schema.emailType
        # add to the list of records
        records += [
            emails.pyre_immutable(id=tokenGenerator(), description="home"),
            emails.pyre_immutable(id=tokenGenerator(), description="work"),
            ]
        # all  done
        return


    def primePhoneTypes(self, tokenGenerator, schema, records, **kwds):
        """
        Create the default phone types
        """
        # pull the phone types
        phones = schema.phoneType
        # add to the list of records
        records += [
            phones.pyre_immutable(id=tokenGenerator(), description="cell"),
            phones.pyre_immutable(id=tokenGenerator(), description="fax"),
            phones.pyre_immutable(id=tokenGenerator(), description="land line"),
            ]
        # all  done
        return


    def primeURITypes(self, tokenGenerator, schema, records, **kwds):
        """
        Create the default uri types
        """
        # pull the uri types
        uris = schema.uriType
        # add to the list of records
        records += [
            uris.pyre_immutable(id=tokenGenerator(), description="web"),
            uris.pyre_immutable(id=tokenGenerator(), description="facebook"),
            uris.pyre_immutable(id=tokenGenerator(), description="instagram"),
            uris.pyre_immutable(id=tokenGenerator(), description="twitter"),
            uris.pyre_immutable(id=tokenGenerator(), description="vine"),
            uris.pyre_immutable(id=tokenGenerator(), description="youtube"),
            ]
        # all  done
        return


    def primePayTypes(self, tokenGenerator, schema, records, **kwds):
        """
        Create the default pay types
        """
        # pull the pay types
        pay = schema.payType
        # add to the list of records
        records += [
            pay.pyre_immutable(id=tokenGenerator(), description="hourly"),
            pay.pyre_immutable(id=tokenGenerator(), description="salary"),
            ]
        # all  done
        return


# end of file
