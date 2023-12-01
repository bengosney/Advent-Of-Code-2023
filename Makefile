.PHONY: help clean test install all init dev
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

HOOKS=$(.git/hooks/pre-commit)
REQS=$(wildcard requirements.*.txt)

PYTHON_VERSION:=$(shell python --version | cut -d " " -f 2)
PIP_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/pip
WHEEL_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/wheel
PIP_SYNC_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/pip-sync
PRE_COMMIT_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/pre-commit

ALLDAYS=$(wildcard src/day_*.py)
ALLINPUTS=$(subst src/,inputs/,$(subst .py,.txt,$(ALLDAYS)))
CURRENT_PY=src/day_$(shell date +%d).py
CURRENT_INPUT=inputs/day_$(shell date +%d).txt
COOKIEFILE=cookies.txt

inputs: $(ALLINPUTS)
	@echo $^

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml:
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/060fd68f4c7dec75e8481e5f5a4232296282779d/.pre-commit-config.yaml > $@
	python -m pip install pre-commit
	pre-commit autoupdate

requirements.%.txt: $(PIP_SYNC_PATH) pyproject.toml
	@echo "Builing $@"
	@python -m piptools compile --generate-hashes --extra $* -q -o $@ $(filter-out $<,$^)

requirements.txt: $(PIP_SYNC_PATH) pyproject.toml
	@echo "Builing $@"
	@python -m piptools compile --generate-hashes -q $(filter-out $<,$^)

.direnv: .envrc
	@touch $@ $^

.git/hooks/pre-commit: $(PRE_COMMIT_PATH) .pre-commit-config.yaml .git
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.11" > $@
	@touch -d '+1 minute' $@
	@false

$(PIP_PATH):
	@python -m ensurepip
	@python -m pip install --upgrade pip
	@touch $@

$(WHEEL_PATH): $(PIP_PATH)
	@python -m pip install wheel
	@touch $@

$(PIP_SYNC_PATH): $(PIP_PATH) $(WHEEL_PATH)
	@python -m pip install pip-tools
	@touch $@

$(PRE_COMMIT_PATH): $(PIP_PATH) $(WHEEL_PATH)
	@python -m pip install pre-commit
	@touch $@

init: .direnv .git/hooks/pre-commit $(PIP_SYNC_PATH) requirements.dev.txt ## Initalise a enviroment

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache .testmondata .install.state

install: $(PIP_SYNC_PATH) requirements.txt $(REQS) ## Install requirements (default)
	@echo "Installing $(filter-out $<,$^)"
	@python -m piptools sync requirements.txt $(REQS)

inputs/day_%.txt: $(COOKIEFILE)
	echo $@
	curl -H 'User-Agent: Makefile - curl : bengosney@googlemail.com' --cookie "$(shell cat $^)" -s -L -o $@ https://adventofcode.com/2023/day/$(shell echo "$@" | egrep -o "[0-9]+" | sed 's/^0*//')/input

src/day_%.py:
	cp template.py.template $@

mypy: $(ALLDAYS)
	mypy --check-untyped-defs $^

pytest: src/*.py
	pytest $^

test: pytest mypy

.install.state: requirements.txt $(REQS)
	@$(MAKE) install
	@touch $@

go: .install.state $(CURRENT_PY) $(CURRENT_INPUT) ## Setup current day and start runing test monitor
	ptw --runner "pytest --testmon" --onfail "notify-send \"Failed\"" --onpass "notify-send \"Passed\"" src/*.py

today: .install.state $(CURRENT_PY) $(CURRENT_INPUT) ## Setup current day and start runing test monitor
	ptw --runner "pytest --testmon" --onfail "notify-send \"Failed\"" --onpass "notify-send \"Passed\"" $(CURRENT_PY)

day_%:
	ptw --runner "pytest --testmon" --onfail "notify-send \"Failed\"" --onpass "notify-send \"Passed\"" src/$@.py
