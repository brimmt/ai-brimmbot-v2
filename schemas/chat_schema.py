from pydantic import BaseModel


class ChatRequestSchema(BaseModel):
    session_id: str
    user_input: str

    class Config():
        orm_mode=True


