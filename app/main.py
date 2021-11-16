from secrets import token_urlsafe
from datetime import datetime, timezone
from html import escape
from urllib.parse import urlparse
from typing import Optional

from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.redis_client import RedisClient
from app.schemas import Message, IncomingMessage
from app.config import Configuration



config = Configuration()

app = FastAPI(title=config.title)
security = HTTPBasic()

redis_client = RedisClient(config.redis)
redis_conn = redis_client.connect()



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
    ):
    """
    Handle request validation exceptions.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            { "error": "required field is missing" }
            )
    )


def generate_message_id(length: int = config.id_length) -> str:
    """
    Return a randomized URL-safe string of n character length.
    """
    return token_urlsafe(length)


def message_is_valid(message):
    """
    Validate message length.
    """
    if config.min_length < len(message) < config.max_length:
        return True
    else:
        return False


def get_base_url(url):
    """
    Parse the base URL out of a Request object.
    """
    url = str(url)
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}"


@app.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Message,
    tags=["messaging"],
    summary="Post a new message",
    response_description="The message item details"
    )
async def post_message(
    request: Request,
    incoming_message: IncomingMessage,
    test_expiry: Optional[int] = None,
    auth: HTTPBasicCredentials = Depends(security)
    ) -> dict:
    """
    Post a new message that will be stored and automatically scheduled for deletion.
    Message contents are accepted as a JSON value in the request body.
    
    `json_body = {"message":
            "Great stories shared and enjoyed by anyone, anywhere and anytime."}`

    The response includes the URL where the message will be accessible, as well as the expiration time.
    """
    correct_username = secrets.compare_digest(auth.username, config.username)
    correct_password = secrets.compare_digest(auth.password, config.password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    message_contents = incoming_message.message
    if not message_is_valid(message_contents):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="malformed message contents"
            )

    message_id = generate_message_id()
    created = int(datetime.now(timezone.utc).timestamp())
    expires = created + test_expiry if test_expiry else created + config.validity_seconds
    message = escape(message_contents)
    url = f"{get_base_url(request.url)}/{message_id}"
    
    message_entry = Message(
        id = message_id,
        created = created,
        expires = expires,
        message = message,
        url = url
    )

    message_entry = message_entry.dict()
    await redis_client.store_and_schedule(message_entry)

    return message_entry


@app.get(
    "/{message_id}",
    status_code=status.HTTP_200_OK,
    response_model=Message,
    tags=["messaging"],
    summary="Fetch a message",
    response_description="Message details"
    )
async def get_message(message_id: str) -> dict:
    """
    Fetches a message by ID if it hasn't expired.
    """
    result = await redis_client.get(message_id)

    if result:
        return result

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid message id"
            )
