"""Runs the SQL files in /sql against BigQuery and writes docs/data.json.

Reads the Google service account key from the GCP_SA_KEY environment variable.
Only counts and averages are saved. No names, phone numbers or transcripts.
"""
import datetime
import decimal
import json
import os
import pathlib
import sys

from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT = "thrio-prod-4258998"
ROOT = pathlib.Path(__file__).resolve().parent.parent


def make_client():
    info = json.loads(os.environ["GCP_SA_KEY"])
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    return bigquery.Client(project=PROJECT, credentials=creds)


def run(client, name):
    sql = (ROOT / "sql" / f"{name}.sql").read_text()
    return [dict(row) for row in client.query(sql).result()]


def plain(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return str(value)


def main():
    client = make_client()
    out = {
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "window_days": 30,
        "kpis": run(client, "kpis")[0],
        "coverage": run(client, "coverage_by_campaign"),
    }
    path = ROOT / "docs" / "data.json"
    path.write_text(json.dumps(out, indent=2, default=plain))
    print("Wrote", path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # fail loudly so the red X shows in GitHub
        print("ERROR:", exc)
        sys.exit(1)
