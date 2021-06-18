from typing import Optional
from enum import Enum
from pydantic import BaseModel


class TransactionStatus(str, Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class CreateTransactionRequest(BaseModel):
    transaction_id: Optional[str]
    value_in_cents: int
    description: str
    customer_id: str
    merchant_id: str
    transaction_timestamp: int
    event_timestamp: Optional[int]
    latitude: float
    longitude: float
    status: Optional[TransactionStatus]
