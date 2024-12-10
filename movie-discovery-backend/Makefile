.PHONY: test coverage run_tests

test:
	pytest --verbose

coverage:
	coverage run -m pytest
	coverage report -m
	coverage html

run_tests: test coverage
	@echo "All tests and coverage reports have been generated."
