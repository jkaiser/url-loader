.PHONY: init
init:
	pip install -r requirements

.PHONY: test
test:
	python -m unittest discover

.PHONY: coverage
coverage:
	coverage run -m unittest discover
	coverage report
	coverage erase

.PHONY: e2e-test
e2e-test:
	PYTHONPATH=. python tests/e2e_tests/simple_load.py
