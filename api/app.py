from flask import Flask, request
import os
from supabase import create_client, Client
from threading import Thread
from dotenv import load_dotenv
import json
import requests

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

WORKER_URL = "https://policyengine-server-worker-70913873059.us-central1.run.app"
#WORKER_URL = "http://127.0.0.1:5001/compute"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return {
        "status": "ok"
    }

@app.route("/compute", methods=["POST"])
def compute():
    options = request.json

    # Add new job to jobs table, status = queued, options=options and get job id
    job = supabase.table("job").insert({
        "status": "queued",
        "options": options,
    }).execute()

    job_id = job.data[0]["id"]

    requests.get(f"{WORKER_URL}?job_id={job_id}")

    return {
        "status": "ok",
        "job_id": job.data[0]["id"]
    }

@app.route("/work-on-queue", methods=["GET"])
def work_on_queue():
    requests.get(WORKER_URL)

    return {
        "status": "ok"
    }