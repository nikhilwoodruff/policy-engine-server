debug-api:
	FLASK_APP=api/app/app.py FLASK_DEBUG=True flask run

debug-worker:
	FLASK_APP=api/worker/worker.py FLASK_DEBUG=True flask run --port 5001
