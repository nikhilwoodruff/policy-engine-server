FROM python:3.10
RUN pip install policyengine flask supabase
CMD [ "gunicorn -b :$PORT app:app" ]