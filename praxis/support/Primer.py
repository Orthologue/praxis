# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
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
            self._buildTenderTypes(plexus=plexus),
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
        # build the records
        records = self._buildCompanyInformation(plexus=plexus)
        # save
        datastore.server.insert(*records)
        # all done
        return


    def primeStaffRecords(self, plexus):
        """
        Prime the database with the initial staff information
        """
        # warn about deficiencies in the data source
        plexus.warning.log('please update the staff records to indicate the employment type')
        # grab the staff records
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
        emails = set()
        phones = set()
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
            entity = schema.crm.entity.pyre_immutable(
                entity = eid,
                type = registrar['entity_types']['people'])
            # save it
            entities.append(entity)

            # build the person
            person = schema.crm.person.pyre_immutable(
                entity = eid,
                first = record.first,
                middle = record.middle,
                last = record.last,
                preferred = record.alias)
            # save it
            persons.append(person)

            # build the employee info
            employee = schema.hr.employee.pyre_immutable(
                employee = eid,
                tin = record.ssn,
                identification = record.dl,
                birthday = record.dob if record.dob else schema.null)
            # save it
            employees.append(employee)

            # build the employment records
            employment = schema.hr.employment.pyre_immutable(
                id = record.id,
                employee = eid,
                employer = company.entity,
                rate = record.rate,
                frequency = registrar["pay_frequencies"][record.frequency],
                pay = registrar["pay_types"][record.type],
                effective = record.hired if record.hired else schema.null,
                until = record.terminated if record.terminated else schema.null,
                # and, until the staff table has this information
                type = registrar["employment_types"]["unknown"])
            # save it
            employments.append(employment)

            # get an id for the home address
            homeId = addresses[record.address]
            # build an address
            home = schema.crm.entityLocation.pyre_immutable(
                entity = eid,
                location = homeId,
                purpose = registrar["contact_purposes"]["personal"],
                effective = record.hired if record.hired else schema.null,
                until = record.terminated if record.terminated else schema.null)
            # save it
            homes.append(home)

            # make an email
            emails.add(record.email)
            # build an email address
            email = schema.crm.entityEmail.pyre_immutable(
                entity = eid,
                email = record.email,
                purpose = registrar["contact_purposes"]["work"],
                effective = record.hired if record.hired else schema.null,
                until = record.terminated if record.terminated else schema.null)
            # save it
            mailto.append(email)

            # make a phone number
            phones.add(record.cell)
            # attach it to this employee
            cell = schema.crm.entityPhone.pyre_immutable(
                entity = eid,
                phone = record.cell,
                type = registrar["phone_types"]["cell"],
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
            schema.crm.location.pyre_immutable(location=key, address=address)
            for address, key in addresses.items())
        # make the phone records
        numbers = (
            schema.crm.phone.pyre_immutable(number=number)
            for number in phones)
        # make the email records
        uris = (
            schema.crm.email.pyre_immutable(email=email)
            for email in emails)
        # and store them
        server.insert(*itertools.chain(locations, numbers, uris))

        # finally, store the employee contact info
        server.insert(*itertools.chain(cells, homes, mailto))

        # all done
        return


    # implementation details
    # types
    def _buildEntityTypes(self, plexus):
        """
        Create the default entity types
        """
        # get the entity type factory
        factory = plexus.datastore.schema.crm.entityType.pyre_immutable
        # the built-in entity types
        yield factory(type='companies', description='entities that are incorporated')
        yield factory(type='people', description='entities that are physical persons')
        # all  done
        return


    def _buildItemTypes(self, plexus):
        """
        Create the default item types
        """
        # get the item type factory
        factory = plexus.datastore.schema.sales.itemType.pyre_immutable
        # the built-in item types
        yield factory(type='products', description='items that are products for sale')
        yield factory(type='services', description='items that are services provided to customers')
        # all  done
        return


    def _buildContactTypes(self, plexus):
        """
        Create the default contact types
        """
        # get the contact type factory
        factory = plexus.datastore.schema.crm.contactType.pyre_immutable
        # build the records; the values are supposed to match names of tables in the current
        # schema that contain contact information
        yield factory(type='emails', description='email information for an entity')
        yield factory(type='locations', description='the physical address of an entity')
        yield factory(type='phones', description='the telephone number of an entity')
        yield factory(type='uris', description='the web home page of an entity')
        # all  done
        return


    def _buildContactPurposes(self, plexus):
        """
        Create the default location types
        """
        # get the location type factory
        factory = plexus.datastore.schema.crm.contactPurpose.pyre_immutable
        # build the records
        yield factory(purpose='personal',
                      description="an entity's personal information")
        yield factory(purpose='work',
                      description="an entity's work information")
        yield factory(purpose='info',
                      description="general information about an entity")
        yield factory(purpose='shipping',
                      description="information about shipping to and from an entity")
        yield factory(purpose='billing',
                       description="information for financial exchanges with an entity")
        # all  done
        return


    def _buildPhoneTypes(self, plexus):
        """
        Create the default phone types
        """
        # get the phone type factory
        factory = plexus.datastore.schema.crm.phoneType.pyre_immutable
        # build the records
        yield factory(type='cell', description='the phone number is a mobile phone')
        yield factory(type='voice', description='the phone number is a land line')
        yield factory(type='fax', description='the phone number is a fax')
        yield factory(type='pager', description='the phone number is a pager')
        # all  done
        return


    def _buildURITypes(self, plexus):
        """
        Create the default uri types
        """
        # get the uri type factory
        factory = plexus.datastore.schema.crm.uriType.pyre_immutable
        # build the records
        yield factory(type='web', descrption='uris that are web pages')
        yield factory(type='facebook', descrption='uris that are facebook pages')
        yield factory(type='instagram', descrption='uris that are instagram pages')
        yield factory(type='twitter', descrption='uris that are twitter handles')
        yield factory(type='vine', descrption='uris that are vine pages')
        yield factory(type='youtube', descrption='uris that are youtube channels or pages')
        # all  done
        return


    def _buildEmploymentTypes(self, plexus):
        """
        Create the default employment types
        """
        # get the pay type factory
        factory = plexus.datastore.schema.hr.employmentType.pyre_immutable
        # build the records
        yield factory(type='unknown', description='missing or not specified')
        yield factory(type='partner', description='partners')
        yield factory(type='full time', description='full time employements')
        yield factory(type='part time', description='part time employements')
        yield factory(type='temporary', description='temporary employements')
        yield factory(type='contractor', description='employees that are contractors')
        yield factory(type='intern', description='employees that are interns')
        # all  done
        return


    def _buildPayTypes(self, plexus):
        """
        Create the default pay types
        """
        # get the pay type factory
        factory = plexus.datastore.schema.hr.payType.pyre_immutable
        # build the records
        yield factory(type='partner', description='partner compensation rules')
        yield factory(type='contractor', description='contractor compensation rules')
        yield factory(type='hourly', description='compensation for hourly employees')
        yield factory(type='salary', description='compensation for salaried employees')
        # all  done
        return


    def _buildPayFrequencies(self, plexus):
        """
        Create the default pay types
        """
        # get the pay type factory
        factory = plexus.datastore.schema.hr.payFrequency.pyre_immutable
        # build the records
        yield factory(frequency='weekly', description='weekly compensation')
        yield factory(frequency='biweekly', description='compensation every two weeks')
        yield factory(frequency='monthly', description='monthly compensation')
        yield factory(frequency='quarterly', description='quarterly compensation')
        yield factory(frequency='annually', description='annual compensation')
        # all  done
        return


    def _buildTenderTypes(self, plexus):
        """
        Create the default phone types
        """
        # get the phone type factory
        factory = plexus.datastore.schema.sales.tenderType.pyre_immutable
        # build the records
        yield factory(type='cash', description='cash')
        yield factory(type='credit', description='credit card')
        yield factory(type='debit', description='debit card')
        yield factory(type='gift', description='gift card')
        yield factory(type='discount', description='discount')
        # all  done
        return


    # contact information
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
        yield schema.crm.entity.pyre_immutable(entity=cid, type=ctype)
        # build the company record
        yield schema.crm.company.pyre_immutable(entity=cid, name=plexus.layout.company)
        # put some address in the table
        addresses = [
            ('1500 MORADA PL, ALTADENA, CA 91001-3232', '1998-02-01', '2001-10-30'),
            ('1335 LA SOLANA DR, ALTADENA, CA 91001-2624', '2001-10-31', '2007-06-22'),
            ('624 6TH ST, MANHATTAN BCH, CA 90266-5817', '2007-06-23', '2013-04-30'),
            ('1855 INDUSTRIAL ST STE 601, LOS ANGELES, CA 90021-1260', '2013-05-01', '2015-04-30'),
            ('2135 E 7TH PL STE 9, LOS ANGELES, CA, 90021-1766', '2015-05-01', schema.null)
            ]

        # now go through them
        for hq, effective, until in addresses:
            # make an id for the HQ location
            hqId = idd()
            # the physical address
            yield schema.crm.location.pyre_immutable(location = hqId, address = hq)
            # gets used for the following purposes
            for purpose in ['info', 'shipping', 'billing']:
                # make it so
                yield schema.crm.entityLocation.pyre_immutable(
                    entity = cid,
                    location = hqId,
                    purpose = registrar['contact_purposes'][purpose],
                    effective = effective,
                    until = until
                )

        # make a new phone number
        phone = schema.crm.phone.pyre_immutable(
            number = '+1 626 394 1114'
            )
        # send it off
        yield phone
        # is
        for kind in [ 'cell', 'voice', 'fax' ]:
            # and is used for
            for purpose in [ 'info', 'billing', 'shipping' ]:
                # make it so
                yield schema.crm.entityPhone.pyre_immutable(
                    entity = cid,
                    phone = phone.number,
                    type = registrar['phone_types'][kind],
                    purpose = registrar['contact_purposes'][purpose],
                    effective = '1998-02-01'
                    )

        # the website
        uri = schema.crm.uri.pyre_immutable(
            uri = 'http://www.{.layout.domain}'.format(plexus)
            )
        # send it off
        yield uri
        # is used by
        yield schema.crm.entityURI.pyre_immutable(
            entity = cid,
            uri = uri.uri,
            type = registrar['uri_types']['web'],
            purpose = registrar['contact_purposes']['info'],
            effective = '1998-02-01'
            )

        # the email addresses
        for purpose in ('info', 'billing', 'shipping'):
            # make the email record
            email = schema.crm.email.pyre_immutable(
                email = '{}@{.layout.domain}'.format(purpose, plexus)
                )
            # send it off
            yield email
            # and a use
            yield schema.crm.entityEmail.pyre_immutable(
                entity = cid,
                email = email.email,
                purpose = registrar['contact_purposes'][purpose],
                effective = '1998-02-01'
                )

        # all done
        return


# end of file
