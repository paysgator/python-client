from src.paysgator.client import PaysgatorClient

api_key = "mk_live_56e2f0dd_fbbfb1df44f4adf7cac5e73e568e38e1fe8787b007bfc89bb99f46e31b05f08d"

wallet_id = "6d0c1446-3c8b-4af6-9261-bbaaeba46557"

client = PaysgatorClient(api_key, wallet_id)

link = client.payment_links.create(
    title="Test Product",
    amount=50.0,
    currency="MZN",
    methods=["MPESA"],
    payment_fields={
        "phoneNumber":"842383770"
    },
    confirm=True,
)

print(link)