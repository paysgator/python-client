# Paysgator Python SDK

Official Python client for the Paysgator API.

## Installation

```bash
pip install paysgator
```

## Usage

```python
from paysgator import PaysgatorClient

client = PaysgatorClient(api_key="YOUR_API_KEY", wallet_id="YOUR_WALLET_ID")

# Create a payment link
link = client.payment_links.create(
    title="My Product",
    amount=100.0,
    currency="MZN",
    return_url="https://example.com/callback"
)
print(link.url)
```
