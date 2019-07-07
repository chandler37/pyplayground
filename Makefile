# If you have difficulty with this Makefile, you might install the latest GNU
# Make via Homebrew (https://brew.sh/) [try `brew install make`] and try again
# using `gmake`. If that doesn't work you might want to install the latest bash
# via `brew install bash` and update your PATH to prefer it over the older
# MacOS-provided bash.

# /bin/sh is the default; we want bash so we can 'source venv/bin/activate':
SHELL := $(shell which bash)

ACTIVATE_VENV := source venv/bin/activate

.PHONY: help
help:
	@echo "Read ./README.md to get started."

# One-time installation of virtualenv globally.
#
# We use `pip3`, not `pip`. On MacOS `pip` is Python 2.7 (either
# via Homebrew `python@2` or, frigteningly, the stock Python provided by
# Apple), not Python 3. `pip3` (using python version 3) is courtesy of the
# `python` package from [Homebrew](https://brew.sh/).
.PHONY: install_virtualenv
install_virtualenv:
	@echo "If brew is not found, you need to install Homebrew; see https://brew.sh/"
	brew update
	brew install python
	pip3 install virtualenv

venv:
	@echo "Install virtualenv system-wide via 'make install_virtualenv' if the following fails:"
	virtualenv -p python3 venv
	@echo "The virtualenv is not active unless you run the following:"
	@echo "source venv/bin/activate"
	@echo ""
	@echo "But if you use the Makefile it activates it for you temporarily."

.PHONY: install
install: venv/installation.success

venv/installation.success: requirements.txt | venv
	$(ACTIVATE_VENV) && pip install -r requirements.txt
	touch $@

.PHONY: shell
shell: | venv/installation.success
	$(ACTIVATE_VENV) && PYTHONSTARTUP=interactive.py ipython

.PHONY: run
run: | venv/installation.success
	$(ACTIVATE_VENV) && python pyplayground-runner.py $(ARGS)

.PHONY: test
test: | venv/installation.success
	$(ACTIVATE_VENV) && python run_tests.py

.PHONY: upgrade
upgrade: unfreezeplus venv/installation.success test
	@echo "The upgraded third-party dependencies might work... at least tests passed."

.PHONY: unfreezeplus
unfreezeplus:
	@git diff-index --quiet HEAD || { echo "not in a clean git workspace; run 'git status'"; exit 1; }
	rm -f venv/installation.success
	# If this fails, `deactivate; make clean` and try again:
	$(ACTIVATE_VENV) && { pip freeze | xargs pip uninstall -y; }
	sed -i "" -e "s/=.*//" requirements.txt
	$(ACTIVATE_VENV) && pip install -r requirements.txt
	$(ACTIVATE_VENV) && pip freeze > requirements.txt

.PHONY: clean
clean:
	rm -fr venv **/*.pyc **/__pycache__ .cache

.DEFAULT_GOAL := help
