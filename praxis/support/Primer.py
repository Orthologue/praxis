# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import itertools
import collections


# class declaration
class Primer:
    """
    Populate a freshly instantiated schema with canonical data
    """


    # interface
    def primeTypes(self, plexus):
        """
        Main entry point that delegates table priming to the more specialized hooks
        """
        # get {chain}
        import itertools
        # walk through the table primers and chain them together
        records = itertools.chain(
            self._buildEntityTypes(plexus=plexus),
            self._buildItemTypes(plexus=plexus),
            self._buildContactTypes(plexus=plexus),
            self._buildContactPurposes(plexus=plexus),
            self._buildPhoneTypes(plexus=plexus),
            self._buildURITypes(plexus=plexus),
            self._buildEmploymentTypes(plexus=plexus),
            self._buildPayTypes(plexus=plexus),
            self._buildPayFrequencies(plexus=plexus),
            )

        # get the datastore
        datastore = plexus.datastore
        # save
        datastore.server.insert(*records)
        # all done
        return


    def primeCompanyInformation(self, plexus):
        """
        Prime the database with the basic client information
        """
        # get the datastore
        datastore = plexus.datastore
        # save
        datastore.server.insert(*self._buildCompanyInformation(plexus=plexus))
        # all done
        return


    def primeStaffRecords(self, plexus):
        """
        Prime the database with the initial staff information
        """
        uri = plexus.layout.staffRecords

        # attempt to
        try:
            # get the location of the CSV file and open it
            stream = plexus.pyre_fileserver.open(uri=plexus.layout.staffRecords)
        # if this fails
        except plexus.FrameworkError:
            # complain
            plexus.warning.log("skipping priming of staff records; uri '{}' is invalid".format(uri))
            # nothing further to do
            return

        # make a parser
        p = plexus.ingest.staff()

        # get the token generator
        idd = plexus.idd
        # the schema
        schema = plexus.schema
        # the datastore
        datastore = plexus.datastore
        # and the registrar
        registrar = plexus.typeRegistrar

        # form the company query
        companyQ = plexus.queries.company(name=plexus.layout.company)
        # to get the company record
        company = list(datastore.select(companyQ))[0]

        # the indices
        emails = collections.defaultdict(idd)
        phones = collections.defaultdict(idd)
        addresses = collections.defaultdict(idd)
        # and the record workload
        entities = []
        persons = []
        employees = []
        employments = []
        cells = []
        homes = []
        mailto = []

        # get the records
        for record in p.read(stream=stream, uri=stream.name):
            # get an entity id
            eid = idd()

            # build the entity
            entity = schema.entity.pyre_immutable(
                eid = eid,
                kind = registrar['entity_types']['persons'])
            # save it
            entities.append(entity)

            # build the person
            person = schema.person.pyre_immutable(
                entity = eid,
                first = record.first,
                middle = record.middle,
                last = record.last,
                preferred = record.alias)
            # save it
            persons.append(person)

            # build the employee info
            employee = schema.employee.pyre_immutable(
                employee = eid,
                tin = record.ssn,
                idn = record.dl,
                dob = record.dob if record.dob else schema.null)
            # save it
            employees.append(employee)

            # build the employment records
            employment = schema.employment.pyre_immutable(
                id = record.id,
                employee = eid,
                employer = company.entity,
                rate = record.rate,
                frequency = registrar["pay_frequencies"][record.frequency],
                type = registrar["pay_types"][record.type],
                effective = record.hired if record.hired else schema.null,
                until = record.terminated if record.terminated else schema.null)
            # save it
            employments.append(employment)

            # get an id for the home address
            homeId = addresses[record.address]
            # build an address
            home = schema.entityLocation.pyre_immutable(
                entity = eid,
                location = homeId,
                purpose = registrar["contact_purposes"]["personal"],
                effective = record.hired if record.hired else schema.null,
                until = record.terminated if record.terminated else schema.null)
            # save it
            homes.append(home)

            # get a token for the email address
            emailId = emails[record.email]
            # build an email address
            email = schema.entityEmail.pyre_immutable(
                entity = eid,
                email = emailId,
                purpose = registrar["contact_purposes"]["work"],
                effective = record.hired if record.hired else schema.null,
                until = record.terminated if record.terminated else schema.null)
            # save it
            mailto.append(email)

            # get a token for the cell
            cellId = phones[record.cell]
            # attach it to this employee
            cell = schema.entityPhone.pyre_immutable(
                entity = eid,
                phone = cellId,
                kind = registrar["phone_types"]["cell"],
                purpose = registrar["contact_purposes"]["work"],
                effective = record.hired if record.hired else schema.null,
                until = record.terminated if record.terminated else schema.null)
            # save it
            cells.append(cell)

        # get the server
        server = datastore.server

        # store the entities; they must be committed before referenced
        server.insert(*entities)
        # store the basic info
        server.insert(*itertools.chain(persons, employees, employments))

        # make the location records
        locations = (
            schema.location.pyre_immutable(id=key, address=address)
            for address, key in addresses.items())
        # make the phone records
        numbers = (
            schema.phone.pyre_immutable(id=key, number=number)
            for number, key in phones.items())
        # make the email records
        uris = (
            schema.email.pyre_immutable(id=key, email=email)
            for email, key in emails.items())
        # and store them
        server.insert(*itertools.chain(locations, numbers, uris))

        # finally, store the employee contact info
        server.insert(*itertools.chain(cells, homes, mailto))

        # all done
        return


    # implementation details
    def _buildEntityTypes(self, plexus):
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


    def _buildItemTypes(self, plexus):
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


    def _buildContactTypes(self, plexus):
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


    def _buildContactPurposes(self, plexus):
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


    def _buildPhoneTypes(self, plexus):
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


    def _buildURITypes(self, plexus):
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


    def _buildEmploymentTypes(self, plexus):
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


    def _buildPayTypes(self, plexus):
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


    def _buildPayFrequencies(self, plexus):
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


    # implementation details
    def _buildCompanyInformation(self, plexus):
        """
        Add the company information to the database table
        """
        # get the token generator
        idd = plexus.idd
        # the connection to the database server
        datastore = plexus.datastore
        # the schema
        schema = plexus.datastore.schema
        # and the category registrar
        registrar = plexus.typeRegistrar

        # grab an entity id
        cid = idd()
        # get my entity type
        ctype = registrar['entity_types']['companies']

        # build a new entity
        yield schema.entity.pyre_immutable(eid=cid, kind=ctype)
        # build the company record
        yield schema.company.pyre_immutable(entity=cid, name=plexus.layout.company)


        addresses = [
            ('1500 MORADA PL, ALTADENA, CA 91001-3232', '1998-02-01', '2001-10-30'),
            ('1335 LA SOLANA DR, ALTADENA, CA 91001-2624', '2001-10-31', '2007-06-22'),
            ('624 6TH STR, MANHATTAN BCH, CA 90266-5817', '2007-06-23', '2013-04-30'),
            ('1855 INDUSTRIAL STR STE 601, LOS ANGELES, CA, 90021-1260', '2013-05-01', schema.null)
            ]

        # now go through them
        for hq, effective, until in addresses:
            # make an id for the HQ location
            hqId = idd()
            # the physical address
            yield schema.location.pyre_immutable(id = hqId, address = hq)
            # gets used for the following purposes
            for purpose in ['info', 'shipping', 'billing']:
                # make it so
                yield schema.entityLocation.pyre_immutable(
                    entity = cid,
                    location = hqId,
                    purpose = registrar['contact_purposes'][purpose],
                    effective = effective,
                    until = until
                )

        # make an id for the landline
        phone = idd()
        # the phone number
        yield schema.phone.pyre_immutable(
            id = phone,
            number = '+1 626 394 1114'
            )
        # is
        for kind in [ 'cell', 'voice', 'fax' ]:
            # and is used for
            for purpose in [ 'info', 'billing', 'shipping' ]:
                # make it so
                yield schema.entityPhone.pyre_immutable(
                    entity = cid,
                    phone = phone,
                    kind = registrar['phone_types'][kind],
                    purpose = registrar['contact_purposes'][purpose],
                    effective = '1998-02-01'
                    )

        # make an id for the URI
        uri = idd()
        # the website
        yield schema.uri.pyre_immutable(
            id = uri,
            uri = 'http://www.{.layout.domain}'.format(plexus)
            )
        # is used by
        yield schema.entityURI.pyre_immutable(
            entity = cid,
            uri = uri,
            kind = registrar['uri_types']['web'],
            purpose = registrar['contact_purposes']['info'],
            effective = '1998-02-01'
            )

        # the email addresses
        for email in ('info', 'billing', 'shipping'):
            # make an id
            eid = idd()
            # make the email record
            yield schema.email.pyre_immutable(
                id = eid,
                email = '{}@{.layout.domain}'.format(email, plexus)
                )
            # and a use
            yield schema.entityEmail.pyre_immutable(
                entity = cid,
                email = eid,
                purpose = registrar['contact_purposes'][email],
                effective = '1998-02-01'
                )

        # all done
        return


# end of file
