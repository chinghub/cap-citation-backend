VENV_DIR=venv
SRC_DIR=src

PYTHON=python
PIP=pip
ACTIVATE_VENV=source $(VENV_DIR)/bin/activate

.DEFAULT_GOAL=build

# ----- targets --------

$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE_VENV) && $(PIP) install -r requirements.txt

setup: $(VENV_DIR)

build: setup

clean:
	rm -rf $(BUILD_DIR)
	find . -name "*.pyc" | xargs rm

cleanall: clean
	rm -rf $(VENV_DIR)

deploy-dev:
	zappa deploy dev

update-dev:
	zappa update dev

launch-dev:
	curl https://pc0jmn7ar5.execute-api.us-west-2.amazonaws.com/dev

run:
	$(ACTIVATE_VENV) && PYTHONPATH=$(SRC_DIR) $(PYTHON) $(SRC_DIR)/cap-citation-service.py
