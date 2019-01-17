all: format test

test:
	pipenv run python -m unittest

format:
	pipenv run yapf -ir . && pipenv run isort -rc
