from src.utils.auth import hash_password, create_access_token, verify, verify_token
from src.utils import errors
from src.schemas import auth as schema
from src.repository import auth as auth_repository


def sign_up(sign_up_input: schema.SignUpInput):
    """
    Sign up a user.
    """
    try:
        repository = auth_repository.AuthRepository()
        if repository.exist_email(sign_up_input.email):
            raise errors.BadRequest("Email already exists.")
        hashed_password = hash_password(sign_up_input.password)
        sign_up_input.password = hashed_password
        user_created = repository.sign_up(sign_up_input)
        token = repository.token_create(create_access_token(user_created.id))
        sign_up_response = schema.SignUpOutput(
            token=token.token,
            email=sign_up_input.email,
        )
        return sign_up_response
    except Exception as e:
        raise e


def sign_in(sign_in_input: schema.SignInInput):
    """
    Sign in a user.
    """
    try:
        repository = auth_repository.AuthRepository()
        user = repository.exist_email(sign_in_input.email)
        if not user:
            raise errors.BadRequest("Invalid credentials.")
        hashed_password = user.password
        verify(sign_in_input.password, hashed_password)
        repository.token_delate(user.id)
        token = repository.token_create(create_access_token(user.id))
        sign_in_response = schema.SignInOutput(
            token=token.token,
            id=user.id,
        )
        return sign_in_response
    except Exception as e:
        raise e


def authenticate(authenticate_input: schema.AuthenticateInput):
    """
    Authenticate a user.
    """
    try:
        repository = auth_repository.AuthRepository()
        token = repository.token_exist(authenticate_input.token)
        if token.is_active is False:
            raise errors.BadRequest("Token is not active.")
        return verify_token(authenticate_input.token)
    except Exception as e:
        raise e