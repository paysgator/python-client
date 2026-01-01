import requests
from typing import Optional, List
from .models import (
    AuthResponse, PaymentLinkCreateRequest, PaymentLinkResponse,
    SubscriptionResponse, SubscriptionUpdateRequest, TransactionResponse,
    WalletBalanceResponse
)
from .exceptions import AuthenticationError, APIError

class Resource:
    def __init__(self, client):
        self.client = client

class PaymentLinks(Resource):
    def create(self, title: str, amount: float, currency: str, **kwargs) -> PaymentLinkResponse:
        data = {
            "title": title,
            "amount": amount,
            "currency": currency,
            **kwargs
        }
        # Validate with pydantic
        request_model = PaymentLinkCreateRequest(**data)
        response_data = self.client.request("POST", "/payment-links", data=request_model.model_dump(by_alias=True, exclude_none=True))
        return PaymentLinkResponse(**response_data)

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

    def __init__(self, api_key: str, wallet_id: str):
        self.api_key = api_key
        self.wallet_id = wallet_id
        self._token = None
        self.session = requests.Session()
        self.payment_links = PaymentLinks(self)
        self.subscriptions = Subscriptions(self)
        self.transactions = Transactions(self)
        self.wallet = Wallet(self)

    def _authenticate(self):
        url =f"{self.BASE_URL}/auth"
        payload = {"apiKey": self.api_key, "walletId": self.wallet_id}
        response = self.session.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            auth_response = AuthResponse(**data)
            self._token = auth_response.access_token
            self.session.headers.update({"Authorization": f"Bearer {self._token}"})
        elif response.status_code in [400, 401]:
             raise AuthenticationError("Invalid API Key or Wallet ID")
        else:
            raise APIError(response.status_code, response.text)

    def request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        if not self._token:
            self._authenticate()
        
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(method, url, json=data)
        
        if response.status_code == 401:
            # Token might have expired, retry once
            self._authenticate()
            response = self.session.request(method, url, json=data)

        if response.status_code >= 400:
             raise APIError(response.status_code, response.text)
        
        return response.json()
