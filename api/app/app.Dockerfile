FROM python:3.10
RUN pip install policyengine flask supabase
COPY . .
EXPOSE 8080
CMD [ "gunicorn" "-b 8080" "app:app" ]