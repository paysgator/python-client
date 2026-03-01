# Paysgator Python SDK

Official Python client for the Paysgator API.

## Installation

```bash
pip install paysgator
```

## Usage

```python
import os; from paysgator import PaysgatorClient
# WARNING: Never hardcode API keys. Use environment variables.
client = PaysgatorClient(api_key=os.getenv("PAYSGATOR_API_KEY"))

# Create a payment
payment = client.payments.create(
    amount=100.0,
    currency="MZN",
    payment_methods=["MPESA", "CARD"],
    return_url="https://example.com/callback"
)
print(f"Payment Link: {payment.data.checkout_url}")
print(f"Transaction ID: {payment.data.transaction_id}")

# Confirm a payment (Server-side)
confirmation = client.payments.confirm(
    payment_link_id="payment_link_uuid",
    payment_method="MPESA",
    payment_fields={"phoneNumber": "841234567"}
)
print(f"Confirmed Transaction: {confirmation.data.transaction_id}")

# Check Balance
balance = client.wallet.get_balance()
print(f"Balance: {balance.balance} {balance.currency}")
```
