venv:
	python3 -m venv env; source env/bin/activate && pip install --upgrade pip && pip install -r requirements/dev.txt

develop:
	env/bin/python setup.py develop

install:
	env/bin/python setup.py install

test:
	pytest tests/

clean:
	rm -rf env