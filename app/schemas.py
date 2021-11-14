from pydantic import BaseModel, HttpUrl


class Message(BaseModel):
    id: str
    created: int
    expires: int
    url: HttpUrl
    message: str

class IncomingMessage(BaseModel):
    message: str
