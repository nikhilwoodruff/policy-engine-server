FROM python:3.10
RUN pip install policyengine flask supabase
COPY . .
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--workers", "4", "--timeout", "3600"]