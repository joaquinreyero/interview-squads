from fastapi import APIRouter

from src.schemas import auth as schema
from src.service import auth as service

router = APIRouter(
    prefix="/api/auth",
    tags=['Authentication']
)


@router.post("/sign-up")
def sign_up(user: schema.SignUpInput):
    """
    Sign up a user.
    """
    return service.sign_up(user)


@router.post("/sign-in")
def sign_in(user: schema.SignInInput):
    """
    Sign in a user.
    """
    return service.sign_in(user)


@router.post("/")
def authenticate(user: schema.AuthenticateInput):
    """
    Authenticate a user.
    """
    return service.authenticate(user)
