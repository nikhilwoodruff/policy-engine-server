FROM python:3.10
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn" , "-b", "0.0.0.0:8080", "app:app"]