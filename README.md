---
date: 2024-04-10T13:23:00.504412
author: AutoGPT <info@agpt.co>
---

# kllamma

To create a single API endpoint that refines a string LLM prompt using the GPT4 model via the OpenAI Python package, follow these steps aligned with the specified tech stack:

1. **Programming Language:** Python
2. **API Framework:** FastAPI
3. **Database:** PostgreSQL (Note: This may not be necessary unless you plan to store the original and refined prompts for tracking or other purposes.)
4. **ORM:** Prisma (Again, this ties into whether you will use a database for prompt management.)

**Implementation Guide:**

- First, ensure you have FastAPI and the OpenAI Python package installed in your environment. If not, install them using pip:
  ```bash
  pip install fastapi uvicorn openai
  ```
- Set up a new FastAPI application. Create a route (endpoint) that accepts a POST request containing a string LLM prompt in its body.
- Inside the route, use the OpenAI Python package to interface with the GPT4 model. This involves importing openai, setting your OpenAI API key, and then using `openai.Completion.create()` with the `model='gpt-4'` and your prompt as parameters.
- Before sending the prompt to GPT-4 for refinement, apply prompt engineering techniques to ensure the prompt is clear, specific, and designed to elicit the most useful and relevant response from GPT-4. This could involve preprocessing the user's prompt to include relevant context or questions that guide the AI.
- Once you receive the response from GPT-4, perform any necessary post-processing to refine the output further, if needed. This could involve cleaning up the response, ensuring it aligns with the original intent, or enhancing clarity.
- Finally, return the refined prompt to the user in the response body of your API call.

This endpoint serves as a powerful tool for improving LLM prompts, leveraging GPT-4's capabilities to refine input prompts for more effective and precise AI interactions. Ensure you handle errors and edge cases, such as excessively long prompts or invalid input, to maintain a robust API.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'kllamma'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
