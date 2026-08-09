from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    password: str
    # nickname: str = ''
    # email: str = ''
    # avatar: str = ''
    # bio: str = ''