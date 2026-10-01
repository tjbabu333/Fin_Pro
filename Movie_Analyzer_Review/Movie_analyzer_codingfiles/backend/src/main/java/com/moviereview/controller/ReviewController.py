from typing import Optional, Dict, Any

import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Body,
    Query,
    status,
)

from fastapi.responses import JSONResponse

from services.review_service import (
    ReviewService,
    ReviewSubmissionException,
    DatabaseException,
)

from services.admin_service import (
    AdminService,
    get_admin_service,
)

from services.review_service import get_review_service


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/reviews",
    tags=["Reviews"],
)

def backend_health_check(admin_service: AdminService):

    if not admin_service.is_backend_healthy():

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Backend service is unhealthy",
        )


def validate_review(movie_id: str, review_text: str):

    if not movie_id or not movie_id.strip():

        raise HTTPException(
            status_code=400,
            detail="Movie ID is required",
        )

    if not review_text or not review_text.strip():

        raise HTTPException(
            status_code=400,
            detail="Review text is required",
        )

async def process_review_submission(
    movie_id: str,
    review_text: str,
    review_service: ReviewService,
):

    validate_review(movie_id, review_text)

    result = review_service.submit_review(
        movie_id,
        review_text,
    )

    if result.success:

        return {
            "review": result.review,
            "message": result.message,
        }

    return JSONResponse(
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        content={
            "review": result.review,
            "message": result.message,
            "warning": "Review analysis completed but storage failed",
        },
    )

@router.get("/{movie_id}")
async def get_reviews(
    movie_id: str,
    admin_service: AdminService = Depends(get_admin_service),
    review_service: ReviewService = Depends(get_review_service),
):

    backend_health_check(admin_service)

    try:

        logger.info(f"GET Reviews {movie_id}")

        reviews = review_service.get_reviews_by_movie_id(
            movie_id
        )

        return reviews

    except DatabaseException as ex:

        raise HTTPException(
            status_code=503,
            detail=str(ex),
        )

    except Exception:

        logger.exception("Unexpected Error")

        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )

@router.post("")
async def submit_review(
    request: Request,
    movieId: Optional[str] = Query(None),
    reviewText: Optional[str] = Query(None),
    body: Optional[Dict[str, Any]] = Body(None),
    admin_service: AdminService = Depends(get_admin_service),
    review_service: ReviewService = Depends(get_review_service),
):

    backend_health_check(admin_service)

    try:

        final_movie = movieId

        final_review = reviewText

        if body:

            final_movie = body.get(
                "movieId",
                final_movie,
            )

            final_review = body.get(
                "reviewText",
                final_review,
            )

        logger.info(
            f"Submit Review : {final_movie}"
        )

        return await process_review_submission(
            final_movie,
            final_review,
            review_service,
        )

    except ReviewSubmissionException as ex:

        raise HTTPException(
            status_code=503,
            detail=str(ex),
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )

    except Exception:

        logger.exception("Unexpected Error")

        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )