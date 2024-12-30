FROM python:3.10
RUN pip install policyengine flask supabase
COPY . .
ENTRYPOINT ["gunicorn" , "-b", "0.0.0.0:8080", "app:app"]