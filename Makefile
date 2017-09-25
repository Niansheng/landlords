VIRTUAL=. devenv/bin/activate && cd landlords
all: doc package

setup: devenv migrate test

devenv:
	tox -e devenv -vv

.PHONY : clean-tox
clean-tox:
	rm -rf devenv .tox

.PHONY : clean-python
clean-python:
	find ./ -name '*.pyc' -delete
	find ./ -name '__pycache__' -delete

.PHONY : clean-package
clean-package:
	rm -rf non-git dist landlord.egg-info

.PHONY: clean-docs
clean-docs:
	cd doc && make clean

.PHONY : clean
clean: clean-tox clean-python

.PHONY : test
test:
	$(VIRTUAL) && python manage.py test

env:
	$(VIRTUAL) && /bin/bash

run:
	$(VIRTUAL) && python manage.py runserver

migrate:
	$(VIRTUAL) && python manage.py migrate

shell:
	$(VIRTUAL) && python manage.py shell

cronjob:
	$(VIRTUAL) && python manage.py installtasks

run-all: cronjob run
