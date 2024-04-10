from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class FeedbackSubmissionResponse(BaseModel):
    """
    Outlines the outcome of a feedback submission attempt, including success status and any pertinent user messages.
    """

    success: bool
    message: str


async def submit_feedback(
    user_id: str, prompt_refinement_id: str, rating: int, comments: Optional[str]
) -> FeedbackSubmissionResponse:
    """
    Endpoint for submitting feedback on prompt refinement quality.

    This function saves the feedback from a user regarding a prompt refinement attempt in the database. Then,
    it returns a response that includes whether the operation was successful and a user-readable message about the action.

    Args:
    user_id (str): The ID of the user submitting the feedback.
    prompt_refinement_id (str): The ID of the prompt refinement that the feedback is about.
    rating (int): Numerical rating for the prompt refinement, typically on a predefined scale (e.g., 1-5).
    comments (Optional[str]): Optional textual feedback providing more detailed insights or suggestions.

    Returns:
    FeedbackSubmissionResponse: Outlines the outcome of a feedback submission attempt, including success status and any pertinent user messages.

    Throws:
    - An exception when the user or prompt refinement doesn't exist to prevent feedback on non-existent entities.
    """
    feedback_submission = await prisma.models.UserFeedback.prisma().create(
        data={
            "userId": user_id,
            "promptRefinementId": prompt_refinement_id,
            "rating": rating,
            "comments": comments,
        }
    )
    if feedback_submission:
        return FeedbackSubmissionResponse(
            success=True, message="Feedback submitted successfully."
        )
    else:
        return FeedbackSubmissionResponse(
            success=False, message="Failed to submit feedback."
        )
