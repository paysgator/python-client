from src.paysgator.client import PaysgatorClient

#Mpesa direct charge test 

api_key = "<Api Key>"

wallet_id = "<Wallet Id>"

client = PaysgatorClient(api_key, wallet_id)

link = client.payment_links.create(
    title="Test Product",
    amount=50.0,
    currency="MZN",
    methods=["MPESA"],
    payment_fields={
        "phoneNumber":""
    },
    confirm=True,
)

print(link)