PYTHON=python2.6

# versions & releases
PAGINATION_RELEASE=50

# targets
all: requirements.stamp

pagination.stamp:
	svn checkout -r$(PAGINATION_RELEASE) http://django-pagination.googlecode.com/svn/trunk/ django-pagination
	cd django-pagination/pagination && ../../Django-1.0.2-final/django/bin/django-admin.py compilemessages
	date > $@

virtualenv.py: virtualenv.release
	wget http://bitbucket.org/ianb/virtualenv/raw/`head -1 $<`/virtualenv.py
	touch $@

python.stamp: virtualenv.py
	rm -rf python
	$(PYTHON) virtualenv.py --no-site-packages python
	date > $@

requirements.stamp: requirements.txt python.stamp
	./python/bin/pip install -r $<
	date > $@
