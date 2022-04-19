run: src/main.py
	python3 src/main.py

clean:
	-rm -f $(UI_DIR)/*.py
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

deps: requirements.txt
	python3 -m pip install -r requirements.txt

lint:
	python3 -m flake8 ./src/

format:
	python3 -m black -l 79 ./src/
