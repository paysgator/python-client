import requests
from typing import Optional, List, Dict, Any
from .models import (
    PaymentCreateRequest, PaymentCreateResponse,
    PaymentConfirmRequest, PaymentConfirmResponse,
    SubscriptionResponse, SubscriptionUpdateRequest, TransactionResponse,
    WalletBalanceResponse
)
from .exceptions import AuthenticationError, APIError

class Resource:
    def __init__(self, client):
        self.client = client

class Payments(Resource):
    def create(self, amount: float, currency: str, **kwargs) -> PaymentCreateResponse:
        data = {
            "amount": amount,
            "currency": currency,
            **kwargs
        }
        request_model = PaymentCreateRequest(**data)
        response_data = self.client.request("POST", "/payment/create", data=request_model.model_dump(by_alias=True, exclude_none=True))
        return PaymentCreateResponse(**response_data)

    def confirm(self, payment_link_id: str, payment_method: str, **kwargs) -> PaymentConfirmResponse:
        data = {
            "paymentLinkId": payment_link_id,
            "paymentMethod": payment_method,
            **kwargs
        }
        request_model = PaymentConfirmRequest(**data)
        response_data = self.client.request("POST", "/payment/confirm", data=request_model.model_dump(by_alias=True, exclude_none=True))
        return PaymentConfirmResponse(**response_data)

class Subscriptions(Resource):
    def update(self, subscription_id: str, action: str) -> SubscriptionResponse:
        request_model = SubscriptionUpdateRequest(action=action)
        response_data = self.client.request("PATCH", f"/subscriptions/{subscription_id}", data=request_model.model_dump(by_alias=True))
        return SubscriptionResponse(**response_data)

class Transactions(Resource):
    def get(self, transaction_id: str) -> TransactionResponse:
        response_data = self.client.request("GET", f"/transactions/{transaction_id}")
        return TransactionResponse(**response_data)

class Wallet(Resource):
    def get_balance(self) -> WalletBalanceResponse:
        response_data = self.client.request("GET", "/wallet/balance")
        return WalletBalanceResponse(**response_data)

class PaysgatorClient:
    BASE_URL = "https://paysgator.com/api/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        })
        
        self.payments = Payments(self)
        self.subscriptions = Subscriptions(self)
        self.transactions = Transactions(self)
        self.wallet = Wallet(self)

    def set_base_url(self, url: str):
        self.BASE_URL = url

    def request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(method, url, json=data)
        
        if response.status_code >= 400:
             raise APIError(response.status_code, response.text)
        
        return response.json()
