# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import praxis


# declaration
class Copyright(praxis.command, family='praxis.actions.copyright'):
    """
    Print out the praxis copyright note
    """


    # class interface
    # interface
    @praxis.export
    def main(self, plexus, argv):
        """
        Print the copyright note of the praxis package
        """
        # invoke the package function
        print(praxis.copyright())
        # all done
        return


# end of file
