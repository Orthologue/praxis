# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import re
# access to support for records
import pyre.records


# class declaration
class Staff:
    """
    Importer of staff information from a standard format
    """


    # interface
    def read(self, stream=None, uri=None, **kwds):
        """
        Load the information in {stream} or {uri} into a collection of records
        """
        # create a reader
        csv = pyre.records.csv()
        # build a reader and return it
        return csv.immutable(layout=self.staff, stream=stream, uri=uri, **kwds)
        

    # implementation details
    # the layout of the file
    class staff(pyre.records.record):
        # the fields
        status = pyre.records.str()
        id = pyre.records.str()
        last = pyre.records.str()
        first = pyre.records.str()
        middle = pyre.records.str()
        alias = pyre.records.str()
        cell = pyre.records.str()
        email = pyre.records.str()
        address = pyre.records.str()
        rate = pyre.records.decimal()
        type = pyre.records.str()

        dob = pyre.records.str()
        dob.format = '%m/%d/%Y'

        ssn = pyre.records.str()
        dl = pyre.records.str()

        hired = pyre.records.date()
        hired.format = '%m/%d/%Y'

        terminated = pyre.records.date()
        terminated.format = '%m/%d/%Y'
        
        @pyre.records.converter(traits=[rate])
        def money(value, stripper=re.compile('[^\d.]')):
            value = ''.join(stripper.split(value))        
            if not value: return 0
            return value

        @pyre.records.converter(traits=[cell])
        def phone(value, stripper=re.compile('[^\d+]')):
            value = ''.join(stripper.split(value))        
            if len(value) == 10:
                value = '+1' + value
            return value

        @pyre.records.converter(traits=[ssn])
        def ssnstrip(value, stripper=re.compile('[^\d]')):
            return ''.join(stripper.split(value))

    
# end of file 
