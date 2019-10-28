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
