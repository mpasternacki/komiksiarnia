# versions & releases
DJANGO_VER=1.0.2
TAGGING_RELEASE=154
PHPSERIALIZE_VER=1.1
PAGINATION_RELEASE=50

# targets
all: django.stamp django-tagging.stamp phpserialize.stamp pagination.stamp md5check .gitignore
copy: do-copy md5check .gitignore

# files
DJANGO_F=Django-$(DJANGO_VER)-final.tar.gz
PHPSERIALIZE_F=phpserialize-$(PHPSERIALIZE_VER).tar.gz

MD5_TARGETS= $(DJANGO_F) $(PHPSERIALIZE_F) django-tagging/tagging/*.py

.gitignore:
	echo $@ > $@
	echo '*.stamp' >> $@
	echo $(DJANGO_F) >> $@
	echo `basename $(DJANGO_F) .tar.gz` >> $@
	echo django >> $@
	echo $(PHPSERIALIZE_F) >> $@
	echo `basename $(PHPSERIALIZE_F) .tar.gz` >> $@
	echo phpserialize >> $@
	echo django-tagging/ >> $@

# upstream packages
django.stamp: $(DJANGO_F)
	tar -xzf $(DJANGO_F)
	ln -s `basename $(DJANGO_F) .tar.gz` django
	date > $@

$(DJANGO_F):
	wget http://media.djangoproject.com/releases/1.0.2/$@


django-tagging.stamp:
	svn checkout -r$(TAGGING_RELEASE) http://django-tagging.googlecode.com/svn/trunk/ django-tagging
	date > $@


phpserialize.stamp: $(PHPSERIALIZE_F)
	tar -xzf $(PHPSERIALIZE_F)
	ln -s `basename $(PHPSERIALIZE_F) .tar.gz` phpserialize
	date > $@

$(PHPSERIALIZE_F):
	wget http://pypi.python.org/packages/source/p/phpserialize/$@

pagination.stamp:
	svn checkout -r$(PAGINATION_RELEASE) http://django-pagination.googlecode.com/svn/trunk/ django-pagination
	cd django-pagination/pagination && ../../Django-1.0.2-final/django/bin/django-admin.py compilemessages
	date > $@

# misc
.PHONY: do-copy md5check md5update
do-copy:
	cp -Rvn $(FROM)/upstream/* .

# sudo port install md5sha1sum
md5check: upstream.md5
	@echo '***'
	@echo '*** CHECKSUM CHECK ***'
	@echo '***'
	md5sum -c upstream.md5

upstream.md5:
	@echo '***'
	@echo '*** RECALCULATING CHECKSUMS ***'
	@echo '*** BEWARE ***'
	@echo '***'
	md5sum $(MD5_TARGETS) > upstream.md5
	@echo '***'
	@echo '*** Stopped.  Run `make'"'"' again to continue. ***'
	@echo '***'
	@false
