build-venv:
		python3 -m venv env; source env/bin/activate

develop:
		python3 setup.py develop

install:
		python3 setup.py install

install-venv:
		env/bin/python setup.py install
