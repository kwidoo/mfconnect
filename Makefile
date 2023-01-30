SHELL := /bin/bash

reserve:
	echo "Create a virtual environment"
	source venv/bin/activate && python connect.py