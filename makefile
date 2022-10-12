install:
	pip install -r requirements.txt

format:
	isort .
	black .