build-venv:
		python3 -m venv env; source env/bin/activate

install:
		python3 setup.py install

install-venv:
		env/bin/python setup.py install
