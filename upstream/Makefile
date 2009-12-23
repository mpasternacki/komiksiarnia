# versions & releases
DJANGO_VER=1.1.1
TAGGING_RELEASE=154
PHPSERIALIZE_VER=1.1
PAGINATION_RELEASE=50

# targets
all: django.stamp django-tagging.stamp phpserialize.stamp pagination.stamp md5check .gitignore
copy: do-copy md5check .gitignore

# files
DJANGO_F=Django-$(DJANGO_VER)-final.tar.gz
PHPSERIALIZE_F=phpserialize-$(PHPSERIALIZE_VER).tar.gz

MD5_TARGETS= $(DJANGO_F) $(PHPSERIALIZE_F) django-tagging/tagging/*.py django-pagination/pagination/*.py

.gitignore:
	@echo $@ > $@
	@echo '*.stamp' >> $@
	@echo $(DJANGO_F) >> $@
	@echo `basename $(DJANGO_F) .tar.gz` >> $@
	@echo django >> $@
	@echo $(PHPSERIALIZE_F) >> $@
	@echo `basename $(PHPSERIALIZE_F) .tar.gz` >> $@
	@echo phpserialize >> $@
	@echo django-tagging/ >> $@
	@echo django-pagination/ >> $@

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
