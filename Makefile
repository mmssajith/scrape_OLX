create_venv:
	python -m venv ./env
venv:
	source env/Scripts/activate
packages:
	python -m pip install --upgrade pip
	pip install -r requirements.txt