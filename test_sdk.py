from paysgator import PaysgatorClient

#Mpesa direct charge test 

import os

api_key = os.environ.get("PAYSGATOR_API_KEY", "<Api Key>")

client = PaysgatorClient(api_key=api_key)

link = client.payments.create(
    amount=50.0,
    currency="MZN",
    payment_methods=["MPESA"],
    return_url="https://example.com/callback"
)

print(link)