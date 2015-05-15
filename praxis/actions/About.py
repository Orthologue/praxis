# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import praxis


# declaration
class About(praxis.command, family='praxis.actions.about'):
    """
    Display information about this application
    """

    # user configurable state
    prefix = praxis.properties.str()
    prefix.tip = "specify the portion of the namespace to display"


    # class interface
    @praxis.export(tip="print the copyright note")
    def copyright(self, plexus):
        """
        Print the copyright note of the praxis package
        """
        # get the lines
        for line in praxis._praxis_copyright.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @praxis.export(tip="print out the acknowledgments")
    def credits(self, plexus):
        """
        Print out the license and terms of use of the praxis package
        """
        # make some space
        plexus.info.line()
        # get the lines
        for line in praxis._praxis_acknowledgments.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @praxis.export(tip="print out the license and terms of use")
    def license(self, plexus):
        """
        Print out the license and terms of use of the praxis package
        """
        # make some space
        plexus.info.line()
        # get the lines
        for line in praxis._praxis_license.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @praxis.export(tip='dump the application configuration namespace')
    def nfs(self, plexus):
        """
        Dump the application configuration namespace
        """
        # get the prefix
        prefix = self.prefix or 'praxis'
        # show me
        plexus.pyre_nameserver.dump(prefix)
        # all done
        return


    @praxis.export(tip="print the version number")
    def version(self, plexus):
        """
        Print the version of the praxis package
        """
        # make some space
        plexus.info.line()
        # invoke the package header and push it to the plexus info channel
        plexus.info.line(praxis._praxis_header)
        # get the framework
        import pyre
        # show its version number also
        plexus.info.line(pyre._pyre_header)
        # flush
        plexus.info.log()
        # all done
        return


    @praxis.export(tip='dump the application virtual filesystem')
    def vfs(self, plexus):
        """
        Dump the application virtual filesystem
        """
        # get the prefix
        prefix = self.prefix or '/praxis'
        # show me
        plexus.vfs[prefix].dump()
        # all done
        return


# end of file
