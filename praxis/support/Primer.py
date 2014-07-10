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
    def primeTypes(self, plexus, **kwds):
        """
        Main entry point that delegates table priming to the more specialized hooks
        """
        # walk through the chain of tables
        yield from self.primeEntityTypes(plexus=plexus, **kwds)
        yield from self.primeItemTypes(plexus=plexus, **kwds)
        yield from self.primeContactTypes(plexus=plexus, **kwds)
        yield from self.primeContactPurposes(plexus=plexus, **kwds)
        yield from self.primePhoneTypes(plexus=plexus, **kwds)
        yield from self.primeURITypes(plexus=plexus, **kwds)
        yield from self.primeEmploymentTypes(plexus=plexus, **kwds)
        yield from self.primePayTypes(plexus=plexus, **kwds)
        yield from self.primePayFrequencies(plexus=plexus, **kwds)

        # all done
        return


    def primeCompanyInformation(self, plexus, **kwds):
        """
        Prime the database with the basic client information
        """
        # don't know what to do...
        return []


    def primeStaffRecords(self, plexus, **kwds):
        """
        Prime the database with the initial staff information
        """
        # don't know what to do...
        return []


    # implementation details
    def primeEntityTypes(self, plexus, **kwds):
        """
        Create the default entity types
        """
        # get the entity type factory
        factory = plexus.datastore.schema.entityType
        # the built-in entity types
        names = [ "companies", "persons" ]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


    def primeItemTypes(self, plexus, **kwds):
        """
        Create the default item types
        """
        # get the item type factory
        factory = plexus.datastore.schema.itemType
        # the built-in item types
        names = ["products", "services"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


    def primeContactTypes(self, plexus, **kwds):
        """
        Create the default contact types
        """
        # get the contact type factory
        factory = plexus.datastore.schema.contactType
        # build the records; the values are supposed to match names of tables in the current
        # schema that contain contact information
        names = ["emails", "locations", "phones", "uris"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


    def primeContactPurposes(self, plexus, **kwds):
        """
        Create the default location types
        """
        # get the location type factory
        factory = plexus.datastore.schema.contactPurpose
        # the built-in location types
        names = ["personal", "work", "info", "shipping", "billing" ]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


    def primePhoneTypes(self, plexus, **kwds):
        """
        Create the default phone types
        """
        # get the phone type factory
        factory = plexus.datastore.schema.phoneType
        # the built-in phone types
        names = ["cell", "voice", "fax", "pager" ]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


    def primeURITypes(self, plexus, **kwds):
        """
        Create the default uri types
        """
        # get the uri type factory
        factory = plexus.datastore.schema.uriType
        # the built-in uri types
        names = ["web", "facebook", "instagram", "twitter", "vine", "youtube"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


    def primeEmploymentTypes(self, plexus, **kwds):
        """
        Create the default employment types
        """
        # get the pay type factory
        factory = plexus.datastore.schema.employmentType
        # the built-in employment types
        names = ["full time", "part time", "temporary", "contractor", "intern"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


    def primePayTypes(self, plexus, **kwds):
        """
        Create the default pay types
        """
        # get the pay type factory
        factory = plexus.datastore.schema.payType
        # the built-in pay types
        names = ["partner", "contractor", "hourly", "salary"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


    def primePayFrequencies(self, plexus, **kwds):
        """
        Create the default pay types
        """
        # get the pay type factory
        factory = plexus.datastore.schema.payFrequency
        # the built-in pay types
        names = ["weekly", "biweekly", "monthly", "quarterly", "annually"]
        # go through the names
        for name in names:
            # and build the records
            yield factory.pyre_immutable(id=plexus.idd(), description=name)
        # all  done
        return


# end of file
