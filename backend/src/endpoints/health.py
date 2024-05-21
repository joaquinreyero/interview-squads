from fastapi import status, APIRouter
import logging
from src.repository.test import TestRepository

router = APIRouter(
    prefix="/api",
    tags=['Health Check']
)

logger = logging.getLogger(__name__)


@router.get("/hello-world", status_code=status.HTTP_200_OK)
async def hello_world():
    """
    Test the health of the service.
    """
    logger.info("Hello World endpoint is called.")
    return {"message": "Hello World!"}


@router.get("/db-health", status_code=status.HTTP_200_OK)
def db_health(name: str):
    """
    Test the health of the database.
    """
    try:
        TestRepository.post_test(name)
        if TestRepository().get_test():
            return {"message": "Database is healthy!"}
        return {"message": "Database is unhealthy!"}
    except Exception as e:
        return {"message": f"Database is unhealthy! {e}"}
