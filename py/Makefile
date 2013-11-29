.PHONY: clean distclean test fulltarball develop test nose production

PYTHON=$(shell which python2.7)
VIRTUALENV_STRING=virtualenv-1.10.1
VIRTUALENV_URL=https://pypi.python.org/packages/source/v/virtualenv/${VIRTUALENV_STRING}.tar.gz

develop: env
	env/bin/pip install --editable . 

production: tmp
ifndef VIRTUALENV_DIR
	@echo "Must pass VIRTUALENV_DIR for production"
	@exit 1
endif
	cd tmp && wget --timestamping --no-check-certificate ${VIRTUALENV_URL} && tar xzf ${VIRTUALENV_STRING}.tar.gz 
	cd tmp/${VIRTUALENV_STRING} && ${PYTHON} ./virtualenv.py --system-site-packages --distribute ${VIRTUALENV_DIR}
	${VIRTUALENV_DIR}/bin/pip install . 
	cd tmp/${VIRTUALENV_STRING} && ${PYTHON} ./virtualenv.py --relocatable ${VIRTUALENV_DIR}

bpython: bin
	env/bin/pip install bpython

test: develop
	env/bin/python -m unittest discover

nose: develop
	env/bin/pip install "nose==1.3.0" "coverage==3.6"
	env/bin/nosetests --with-coverage --cover-package=checklauncher --cover-xml --cover-xml-file=tmp/coverage.xml --with-xunit --xunit-file=tmp/nosetests.xml

tmp:
	mkdir -p tmp

env: tmp
	mkdir -p env
	cd tmp && wget --timestamping --no-check-certificate ${VIRTUALENV_URL} && tar xzf ${VIRTUALENV_STRING}.tar.gz 
	cd tmp/${VIRTUALENV_STRING} && ${PYTHON} ./virtualenv.py --system-site-packages --distribute ../../env


clean:
	rm -rf build dist *.egg-info tarballs srpms tmp/coverage.xml tmp/nosetests.xml
	find . \( -name "*.pyc" -o -name "*.pyo" \) -delete

distclean: clean
	rm -rf env tmp

fulltarball: 
# change this for non-hg projects.
ifndef FULLTARBALL
	@echo "Must pass FULLTARBALL filename for fulltarball"
	@exit 1
endif
	mkdir -p tarballs
	hg archive -t tgz tarballs/${FULLTARBALL}.tar.gz
