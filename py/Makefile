.PHONY: clean distclean test fulltarball develop test nose production

PYTHON=$(shell which python2.7)
VIRTUALENV_STRING=virtualenv-1.10.1
VIRTUALENV_URL=https://pypi.python.org/packages/source/v/virtualenv/${VIRTUALENV_STRING}.tar.gz

develop: bin
	bin/pip install --editable . 

production: tmp
ifndef VIRTUALENV_DIR
	@echo "Must pass VIRTUALENV_DIR for production"
	@exit 1
endif
	cd tmp && wget --no-check-certificate ${VIRTUALENV_URL} && tar xzf ${VIRTUALENV_STRING}.tar.gz 
	cd tmp/${VIRTUALENV_STRING} && ${PYTHON} ./virtualenv.py --system-site-packages --distribute ${VIRTUALENV_DIR}
	${VIRTUALENV_DIR}/bin/pip install . 
	cd tmp/${VIRTUALENV_STRING} && ${PYTHON} ./virtualenv.py --relocatable ${VIRTUALENV_DIR}

bpython: bin
	bin/pip install bpython

test: develop
	bin/python -m unittest discover

nose: develop
	bin/pip install "nose==1.3.0" "coverage==3.6"
	bin/nosetests --with-coverage --cover-package=checklauncher --cover-xml --cover-xml-file=tmp/coverage.xml --with-xunit --xunit-file=tmp/nosetests.xml

bin: tmp env
	cd tmp && wget --no-check-certificate ${VIRTUALENV_URL} && tar xzf ${VIRTUALENV_STRING}.tar.gz 
	cd tmp/${VIRTUALENV_STRING} && ${PYTHON} ./virtualenv.py --system-site-packages --distribute ../../env

tmp:
	mkdir -p tmp

env:
	mkdir -p env

clean:
	rm -rf build dist *.egg-info tarballs srpms tmp/coverage.xml tmp/nosetests.xml
	find . \( -name "*.pyc" -o -name "*.pyo" \) -delete

distclean: clean
	rm -rf bin include lib local tmp share man

fulltarball: 
# change this for non-hg projects.
ifndef FULLTARBALL
	@echo "Must pass FULLTARBALL filename for fulltarball"
	@exit 1
endif
	mkdir -p tarballs
	hg archive -t tgz tarballs/${FULLTARBALL}.tar.gz
