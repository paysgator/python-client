from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class Mode(str, Enum):
    LIVE = "LIVE"
    TEST = "TEST"

class SubscriptionAction(str, Enum):
    CANCEL = "cancel"
    PAUSE = "pause"
    RESUME = "resume"

class AuthResponse(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    expires_in: int = Field(..., alias="expiresIn")
    mode: Mode

class PaymentLinkCreateRequest(BaseModel):
    title: str
    amount: float
    currency: str
    description: Optional[str] = None
    return_url: Optional[str] = Field(None, alias="returnUrl")
    fields: Optional[List[str]] = None
    methods: Optional[List[str]] = None
    confirm: Optional[bool] = None
    payment_fields: Optional[dict] = None

class PaymentLinkResponse(BaseModel):
    id: str
    url: str
    status: str
    mode: str

class SubscriptionUpdateRequest(BaseModel):
    action: SubscriptionAction

class SubscriptionResponse(BaseModel):
    id: str
    status: str
    customer_email: Optional[str] = Field(None, alias="customerEmail")
    current_period_end: Optional[str] = Field(None, alias="currentPeriodEnd")

class TransactionResponse(BaseModel):
    id: str
    amount: float
    currency: str
    status: str
    method: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    mode: str

class WalletBalanceResponse(BaseModel):
    wallet_id: str = Field(..., alias="walletId")
    currency: str
    balance: str
    mode: str
