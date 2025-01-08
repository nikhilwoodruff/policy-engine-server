import streamlit as st
import requests
import json
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time
import pandas as pd
import plotly
# streamlit full width
st.set_page_config(layout="wide")

st.title("PolicyEngine API")

API = f"https://policyengine-server-api-70913873059.us-central1.run.app"

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

st.write("This is a playground for the PolicyEngine API. You can use this API to compute the impact of public policy.")

left, right = st.columns(2)

job_id = None

with left:
    country = st.selectbox("Select a country", ["uk", "us"])
    scope = st.selectbox("Select a scope", ["macro", "household"])

    if scope == "household":
        data = st.text_area("Enter a household JSON", value='{}')
        data = json.loads(data)
    else:
        data = st.selectbox("Select a dataset", {
            "uk": ["enhanced_frs", "frs"],
            "us": ["enhanced_cps", "cps"]
        }[country])

    non_default_baseline = st.checkbox("Use non-default baseline")

    if non_default_baseline:
        baseline = st.text_area("Enter a baseline JSON", value='{}')

    non_default_reform = st.checkbox("Use non-default reform")

    if non_default_reform:
        reform = st.text_area("Enter a reform JSON", value='{}')

    time_period = st.selectbox("Select a time period", list(range(2025, 2030)))

    options = "{}"
    kwargs = "{}"

    with st.expander("Advanced"):
        options = st.text_area("Options", "{}", help="Enter a JSON object with options for the simulation")
        kwargs = st.text_area("Key word arguments", "{}", help="Enter a JSON object with kwargs for the simulation calculate call.")

    path = st.text_input("Calculation path", "", help="Leave empty for default. E.g. /macro/comparison/budget")

    if st.button("Compute impact"):
        response = requests.post(
            f"{API}/compute",
            json={
                "country": country,
                "scope": scope,
                "data": data,
                "baseline": baseline if non_default_baseline else None,
                "reform": reform if non_default_reform else None,
                "time_period": time_period,
                "options": json.loads(options) if options else None,
                "kwargs": json.loads(kwargs) if kwargs else None,
                "path": path,
            }
        )

        result = response.json()
        job_id = result.get("job_id")

with right:
    jobs = supabase.table("job").select("*").order("id", desc=True).execute().data
    job_ids = [job["id"] for job in jobs]
    job_id = st.selectbox("Select a job", [None] + job_ids, index=job_ids.index(job_id) + 1 if job_id in job_ids else 0)
    if job_id is not None:
        status = "queued"
        job = None
        with st.spinner("Queued"):
            while status == "queued":
                job = supabase.table("job").select("*").eq("id", job_id).execute()

                if len(job.data) == 0:
                    status = "queued"
                    print("no data, queued")
                
                else:
                    job = job.data[0]
                    status = job["status"]
                    print("data, status", status)
                
                time.sleep(1)
        with st.spinner("Running"):
            while status == "running":
                job = supabase.table("job").select("*").eq("id", job_id).execute()
                
                job = job.data[0]
                status = job["status"]
                print("running", status)
                
                time.sleep(1)
        if status == "complete" or status == "error":
            if status == "error":
                st.error(job["result"]["error"])
            if status == "complete":
                result = job["result"]
            
            if "data" in result and "layout" in result:
                json_data = json.loads(result)
                chart = plotly.graph_objects.Figure(
                    **json_data
                )
                st.write(chart)
            else:
                st.json(result)