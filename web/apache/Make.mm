# -*- Makefile -*-
#
# michael a.g. aivazis
# orthologue
# (c) 1998-2014 all rights reserved
#


include praxis.def
# the package name
PACKAGE = apache
# the stuff in this directory goes to {etc/praxis/apache}
EXPORT_ETCDIR = $(EXPORT_ROOT)/etc/$(PROJECT)
# the apache configuration files
APACHE_CONF = \
    $(PROJECT).conf \
# the list of files
EXPORT_ETC = $(APACHE_CONF)

# the standard build targets
all: export

# make sure we scope the files correctly
export:: export-package-etc

# install
install: tidy
	$(RSYNC) $(RSYNCFLAGS) $(APACHE_CONF) $(APACHE_CONFIGURL)
	ssh $(APACHE_USERURL) 'addgroup $(APACHE_USER) {project.name}'
	ssh $(APACHE_USERURL) 'a2ensite {project.name}'

# deploy
deploy:
	ssh $(APACHE_USERURL) 'service apache2 restart'


# end of file
