import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.submit_feedback_service
import project.submit_prompt_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="kllamma",
    lifespan=lifespan,
    description="To create a single API endpoint that refines a string LLM prompt using the GPT4 model via the OpenAI Python package, follow these steps aligned with the specified tech stack:\n\n1. **Programming Language:** Python\n2. **API Framework:** FastAPI\n3. **Database:** PostgreSQL (Note: This may not be necessary unless you plan to store the original and refined prompts for tracking or other purposes.)\n4. **ORM:** Prisma (Again, this ties into whether you will use a database for prompt management.)\n\n**Implementation Guide:**\n\n- First, ensure you have FastAPI and the OpenAI Python package installed in your environment. If not, install them using pip:\n  ```bash\n  pip install fastapi uvicorn openai\n  ```\n- Set up a new FastAPI application. Create a route (endpoint) that accepts a POST request containing a string LLM prompt in its body.\n- Inside the route, use the OpenAI Python package to interface with the GPT4 model. This involves importing openai, setting your OpenAI API key, and then using `openai.Completion.create()` with the `model='gpt-4'` and your prompt as parameters.\n- Before sending the prompt to GPT-4 for refinement, apply prompt engineering techniques to ensure the prompt is clear, specific, and designed to elicit the most useful and relevant response from GPT-4. This could involve preprocessing the user's prompt to include relevant context or questions that guide the AI.\n- Once you receive the response from GPT-4, perform any necessary post-processing to refine the output further, if needed. This could involve cleaning up the response, ensuring it aligns with the original intent, or enhancing clarity.\n- Finally, return the refined prompt to the user in the response body of your API call.\n\nThis endpoint serves as a powerful tool for improving LLM prompts, leveraging GPT-4's capabilities to refine input prompts for more effective and precise AI interactions. Ensure you handle errors and edge cases, such as excessively long prompts or invalid input, to maintain a robust API.",
)


@app.post(
    "/feedback/submit",
    response_model=project.submit_feedback_service.FeedbackSubmissionResponse,
)
async def api_post_submit_feedback(
    user_id: str, prompt_refinement_id: str, rating: int, comments: Optional[str]
) -> project.submit_feedback_service.FeedbackSubmissionResponse | Response:
    """
    Endpoint for submitting feedback on prompt refinement quality.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(
            user_id, prompt_refinement_id, rating, comments
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/prompt/refine",
    response_model=project.submit_prompt_service.PromptRefinementResponse,
)
async def api_post_submit_prompt(
    prompt: str,
) -> project.submit_prompt_service.PromptRefinementResponse | Response:
    """
    Endpoint for submitting an LLM prompt to be refined.
    """
    try:
        res = await project.submit_prompt_service.submit_prompt(prompt)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
