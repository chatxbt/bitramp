from fastapi import FastAPI, HTTPException, Query, Depends, Request, Response
from fastapi_simple_security import api_key_router, api_key_security
from api.libs.partna.helpers import make_request
from api.libs.cf.workflows.main_flow import process_request
from api.libs.partna.off_ramp import (verify_signature,
                                      process_payment_created,
                                      process_payment_updated,
                                      process_transaction_updated,
                                      CurrencyRateResponse)


async def on_startup():
    pass


description = "BitRamp is a ChatXBT powered web application that can handle off ramping request"

app = FastAPI(
    title="BitRamp",
    description=description,
    version="0.1",
    on_startup=[on_startup],
    openapi_url="/openapi.yaml",
)

app.include_router(api_key_router, prefix="/auth", tags=["_auth"])


@app.get("/")
def read_root():
    return description


# AUTH

@app.get("/secure", dependencies=[Depends(api_key_security)])
async def secure_endpoint():
    """A valid access token is required to access this route"""
    return {"message": "This is a secure endpoint"}


@app.get("/coin/get-rates/{currency}", name="Get Currency Rate", dependencies=[Depends(api_key_security)],
         )
async def get_currency_rate(currency: str):
    currency = await make_request("GET", f"currency/rate", params={"currency": currency})

    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency


@app.get("/agent/chat/{message}", name="Chat Agent", dependencies=[Depends(api_key_security)],
         )
async def get_currency_rate(message: str):
    reply = process_request(message)

    if not reply:
        raise HTTPException(status_code=404, detail="message failed")
    return reply


@app.post("/partna/webhook")
async def handle_webhook(request: Request):
    # Retrieve payload and signature
    payload = await request.json()
    signature = payload.get("signature")

    # Verify the signature
    if not verify_signature(payload.get("data"), signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Process events based on type
    event_type = payload.get("event")
    event_data = payload.get("data")
    if event_type == "Payment Created":
        process_payment_created(event_data)
    elif event_type == "Payment Updated":
        await process_payment_updated(event_data)
    elif event_type == "Transaction updated":
        process_transaction_updated(event_data)

    return {"message": "Event received"}


# Run the app with: uvicorn filename:app --reload

