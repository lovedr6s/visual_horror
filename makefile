lint: 
	uv run flake8 . --exclude=.venv,__pycache__,.git

play:
	uv run main.py