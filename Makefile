debug-api:
	FLASK_APP=api/app/app.py FLASK_DEBUG=True flask run

debug-worker:
	FLASK_APP=api/worker/app.py FLASK_DEBUG=True flask run --port 5001
