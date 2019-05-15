# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
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
    def copyright(self, plexus, **kwds):
        """
        Print the copyright note of the praxis package
        """
        # log the copyright note
        plexus.info.log(praxis.meta.copyright)
        # all done
        return


    @praxis.export(tip="print out the acknowledgments")
    def credits(self, plexus, **kwds):
        """
        Print out the license and terms of use of the praxis package
        """
        # log the acknowledgments
        plexus.info.log(praxis.meta.acknowledgments)
        # all done
        return


    @praxis.export(tip="print out the license and terms of use")
    def license(self, plexus, **kwds):
        """
        Print out the license and terms of use of the praxis package
        """
        # log the license
        plexus.info.log(praxis.meta.license)
        # all done
        return


    @praxis.export(tip='dump the application configuration namespace')
    def nfs(self, plexus, **kwds):
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
    def version(self, plexus, **kwds):
        """
        Print the version of the praxis package
        """
        # log the version number
        plexus.info.line(praxis.meta.banner)
        # get the framework
        import pyre
        # show its version number also
        plexus.info.line(pyre.meta.banner)
        # flush
        plexus.info.log()
        # all done
        return


    @praxis.export(tip='dump the application virtual filesystem')
    def vfs(self, plexus, **kwds):
        """
        Dump the application virtual filesystem
        """
        # get the prefix
        prefix = self.prefix or '/praxis'
        # build the report
        report = '\n'.join(plexus.vfs[prefix].dump())
        # sign in
        plexus.info.line('vfs: prefix={!r}'.format(prefix))
        # dump
        plexus.info.log(report)
        # all done
        return


# end of file
