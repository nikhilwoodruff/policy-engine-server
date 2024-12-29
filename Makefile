debug:
	FLASK_APP=api/app.py FLASK_DEBUG=True flask run

debug-compute:
	FLASK_APP=api/worker.py FLASK_DEBUG=True flask run --port 5001
