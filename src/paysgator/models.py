from typing import List, Optional, Dict, Any, Union
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field

class Mode(str, Enum):
    LIVE = "LIVE"
    TEST = "TEST"

class PaymentCreateRequest(BaseModel):
    amount: Decimal
    currency: str
    external_transaction_id: Optional[str] = Field(None, alias="externalTransactionId")
    payment_methods: Optional[List[str]] = Field(None, alias="paymentMethods")
    fields: Optional[List[str]] = None
    return_url: Optional[str] = Field(None, alias="returnUrl")
    metadata: Optional[Dict[str, Any]] = None

class PaymentCreateResponseData(BaseModel):
    paymentlink_id: str = Field(..., alias="paymentlinkId")
    checkout_url: str = Field(..., alias="checkoutUrl")
    transaction_id: str = Field(..., alias="transactionId")

class PaymentCreateResponse(BaseModel):
    success: bool
    data: PaymentCreateResponseData

class Customer(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None

class PaymentConfirmRequest(BaseModel):
    payment_link_id: str = Field(..., alias="paymentLinkId")
    payment_method: str = Field(..., alias="paymentMethod")
    payment_fields: Optional[Dict[str, Any]] = Field(None, alias="paymentFields")
    customer: Optional[Customer] = None

class PaymentConfirmResponseData(BaseModel):
    transaction_id: str = Field(..., alias="transactionId")
    fee: Decimal
    net_amount: Decimal = Field(..., alias="netAmount")

class PaymentConfirmResponse(BaseModel):
    success: bool
    data: PaymentConfirmResponseData

class SubscriptionAction(str, Enum):
    CANCEL = "cancel"
    PAUSE = "pause"
    RESUME = "resume"

class SubscriptionUpdateRequest(BaseModel):
    action: SubscriptionAction

class SubscriptionResponse(BaseModel):
    id: str
    status: str
    customer_email: Optional[str] = Field(None, alias="customerEmail")
    current_period_end: Optional[str] = Field(None, alias="currentPeriodEnd")

class TransactionResponse(BaseModel):
    id: str
    amount: Decimal
    currency: str
    status: str
    method: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    mode: str

class WalletBalanceResponse(BaseModel):
    wallet_id: str = Field(..., alias="walletId")
    currency: str
    balance: Decimal
    mode: str
