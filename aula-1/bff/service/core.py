from enum import Enum
from pydantic import BaseModel


class CreateTransactionRequest(BaseModel):
    value_in_cents: int
    description: str
    customer_id: str
    merchant_id: str
    transaction_timestamp: int
    latitude: float
    longitude: float


class TransactionStatus(str, Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'
    
