debug-api:
	FLASK_APP=api/app.py FLASK_DEBUG=True flask run

debug-worker:
	FLASK_APP=worker/app.py FLASK_DEBUG=True flask run --port 5001

debug-client:
	streamlit run client/app.py