FROM python:3.10
RUN pip install policyengine flask supabase
COPY . .
CMD [ "gunicorn -b :$PORT app:app" ]