# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import praxis


# declaration
class Version(praxis.command, family='praxis.actions.version'):
    """
    Print out the version of the praxis package
    """


    # interface
    @praxis.export
    def main(self, plexus, argv):
        """
        Print the version of the praxis package
        """
        # invoke the package function
        print(praxis._praxis_header)
        # all done
        return


# end of file 
