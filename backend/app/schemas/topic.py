from pydantic import BaseModel
class Topic(BaseModel):
    subject: str
    topic: str