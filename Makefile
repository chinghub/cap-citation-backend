VENV_DIR=venv
SRC_DIR=src

PYTHON=python
PIP=pip
ACTIVATE_VENV=source $(VENV_DIR)/bin/activate

.DEFAULT_GOAL=build

# ----- targets --------

$(VENV_DIR): requirements.txt
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE_VENV) && $(PIP) install -r requirements.txt
	touch $(VENV_DIR)

git-hooks:
	cp tools/git-hooks/* .git/hooks/

setup: $(VENV_DIR) git-hooks

format:
	$(ACTIVATE_VENV) && black $(SRC_DIR)

pyflakes:
	$(ACTIVATE_VENV) && PYTHONPATH=src/ && pyflakes src/

# static analysis
check: setup pyflakes # style
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && $(PYTHON) -m compileall .
	#$(ACTIVATE_VENV) && PYTHONPATH=src/ $(PYTHON) $(SRC_DIR)/cap-citation-service.py check

test: setup check
	$(ACTIVATE_VENV) && cd $(SRC_DIR)  && STAGE=DEV coverage run -m unittest discover
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && coverage report  --omit '*/venv/*,*test_*,*/lib/*' --fail-under=1 -m --skip-covered
	$(ACTIVATE_VENV) && cd $(SRC_DIR) && coverage html --omit '*/venv/*,*test_*'


build: setup test
	$(ACTIVATE_VENV) && zappa package production

clean:
	rm -rf $(BUILD_DIR)
	find . -name "*.pyc" | xargs rm

cleanall: clean
	rm -rf $(VENV_DIR)

deploy-dev:
	$(ACTIVATE_VENV) && zappa deploy dev

update-dev:
	$(ACTIVATE_VENV) && zappa update dev

launch-dev:
	curl https://pc0jmn7ar5.execute-api.us-west-2.amazonaws.com/dev

run: setup
	$(ACTIVATE_VENV) && PYTHONPATH=$(SRC_DIR) $(PYTHON) $(SRC_DIR)/cap-citation-service.py
