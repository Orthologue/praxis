# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import praxis


# declaration
class License(praxis.command, family='praxis.actions.license'):
    """
    Print out the license and terms of use of the praxis package
    """


    # class interface
    @praxis.export
    def main(self, plexus, argv):
        """
        Print out the license and terms of use of the praxis package
        """
        # invoke the package function
        print(praxis.license())
        # all done
        return


# end of file 
