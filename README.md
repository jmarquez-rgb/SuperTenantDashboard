# Demo dashboard

A GitHub page that shows real numbers from the NCC demo tenant (4258998).

## How it works
1. A GitHub Action runs every 30 minutes (or when you click Run).
2. It asks BigQuery for counts and averages, using the files in `sql/`.
3. It saves them in `docs/data.json`.
4. The page in `docs/index.html` reads `data.json` and swaps in the real numbers.

Only counts and averages are saved. No names, phone numbers or transcripts.

## The one secret
Name: `GCP_SA_KEY`
Where: Settings > Secrets and variables > Actions > New repository secret
What goes in it: the whole contents of a Google service account JSON key file.
That account needs BigQuery Data Viewer on dataset `4258998` and BigQuery Job User on project `thrio-prod-4258998`.

Never put the key in a file, a commit, or a chat.

## What is real and what is sample
Real: voice volume, handle time, talk, hold, wrap-up, abandon rate, transfer rate, summary coverage.
Sample: everything else.

## Known limits
- BigQuery only has a call after it is dispositioned. Live views stay sample data.
- Wrap-up time includes the wait for the AI summary (about 30 s on the long template).
- Handle time ignores calls left undispositioned for over an hour.
