import streamlit as st
import requests
import json
from supabase import create_client, Client
import os
from dotenv import load_dotenv

st.title("PolicyEngine API demo")

API = f"https://policyengine-server-api-70913873059.us-central1.run.app"

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

st.write("This is a demo of the PolicyEngine API. You can use this API to compute the impact of public policy.")

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

time_period = st.selectbox("Select a time period", list(range(2024, 2030)))

path = st.text_input("Calculation path", "")

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
            "path": path,
        }
    )

job_ids = [x["id"] for x in supabase.table("job").select("id").execute().data]
job = st.selectbox("Job", sorted(job_ids))

result = supabase.table("job").select("*").eq("id", job).execute().data[0]

st.json(result)