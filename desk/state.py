import operator
from typing import Annotated, Literal, Optional, TypedDict

try:
    from pydantic import BaseModel, Field  # pyright: ignore[reportMissingImports]
except ImportError:  # pragma: no cover - allows the module to load without pydantic installed
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def Field(*args, **kwargs):
        return args[0] if args else None


class Claim(BaseModel):
    order_id: Optional[str] = Field(description="Order id such as HS2291, or null if the message has none")
    pincode: Optional[str] = Field(description="6-digit pickup pincode, or null if the message has none")
    issue_type: Literal["wrong_size", "defect", "changed_mind", "other"] = Field(description="What the customer says is wrong")
    wants: Literal["exchange", "refund", "unclear"] = Field(description="What the customer asks for")


class Tone(BaseModel):
    tone: Literal["calm", "upset", "angry"] = Field(description="How the customer sounds in the message")


class DeskState(TypedDict):
    message: str

    claim: dict
    tone: str

    messages: Annotated[list, operator.add]
    trips: int

    exit: Literal["approve", "decline", "escalate"]
    reason: str
    action: str
    reply: str
    status: str