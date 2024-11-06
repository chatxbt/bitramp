from controlflow import tool
from api.libs.partna.helpers import make_request

@tool(
    instructions="""
    Retrieve the balance of a merchant account for a specified currency. 
    Example: retrieve_merchant_balance('USD')
    """
)
def retrieve_merchant_balance(currency: str):
    """Get merchant account balance for a specified currency."""
    return make_request("GET", "balance", params={"currency": currency})

@tool(
    instructions="""
    Retrieve details of a merchant account. Example: 
    retrieve_merchant_record()
    """
)
def retrieve_merchant_record():
    """Get merchant account details."""
    return make_request("GET", "merchants")

@tool(
    instructions="""
    Update merchant account details. Example: 
    update_merchant_record(callback_url='https://example.com', logo='https://example.com/logo.png', credit_currency='USD')
    """
)
def update_merchant_record(callback_url: str = None, logo: str = None, credit_currency: str = None):
    """Update specified merchant account details."""
    data = {key: value for key, value in locals().items() if value is not None}
    return make_request("PUT", "merchants", json=data)

@tool(
    instructions="""
    Make a mock payment for testing purposes. 
    Example: make_mock_payment(amount=10.0, currency='USD', payment_method='credit_card')
    """
)
def make_mock_payment(amount: float, currency: str, payment_method: str):
    """Initiate a mock payment."""
    data = {
        "amount": amount,
        "currency": currency,
        "payment_method": payment_method
    }
    return make_request("POST", "mock-payment", json=data)


# ================== Off Ramp =================================

@tool(
    instructions="""
    Create a payment for a specified transaction. Example:
    create_payment(business_id='biz123', incoming_amount=100.0, outgoing_amount=95.0, 
                   incoming_currency='USD', outgoing_currency='NGN', customer_email='customer@example.com', 
                   payment_type='bank', country='NG', account_number='123456789', account_name='John Doe', 
                   bank='Some Bank', bank_code='001')
    """
)
def create_payment(
    business_id: str, incoming_amount: float, outgoing_amount: float,
    incoming_currency: str, outgoing_currency: str, customer_email: str,
    payment_type: str, reference: str = None, rate_key: str = None,
    coinprofile_username: str = None, country: str = None, account_number: str = None,
    account_name: str = None, bank: str = None, bank_code: str = None
):
    """Create a payment transaction."""
    data = {
        "businessId": business_id,
        "incomingAmount": incoming_amount,
        "outgoingAmount": outgoing_amount,
        "incomingCurrency": incoming_currency,
        "outgoingCurrency": outgoing_currency,
        "customerEmail": customer_email,
        "paymentType": payment_type,
        "reference": reference,
        "rateKey": rate_key,
        "coinprofileUsername": coinprofile_username,
        "country": country,
        "accountNumber": account_number,
        "accountName": account_name,
        "bank": bank,
        "bankCode": bank_code,
    }
    # Filter out None values
    data = {key: value for key, value in data.items() if value is not None}
    return make_request("POST", "payment", json=data)


@tool(
    instructions="""
    Retrieve details for a specific payment by its ID. Example:
    get_payment_by_id(payment_id='abc123')
    """
)
def get_payment_by_id(payment_id: str):
    """Get details for a specific payment."""
    return make_request("GET", f"payment/{payment_id}")


@tool(
    instructions="""
    Retrieve details of a specific transaction by its ID. Example:
    get_transaction_by_id(transaction_id='txn123')
    """
)
def get_transaction_by_id(transaction_id: str):
    """Get details for a specific transaction."""
    return make_request("GET", f"transaction/{transaction_id}")


@tool(
    instructions="""
    Retrieve current conversion rates for a specified currency. Example:
    get_current_rates(currency='USD')
    """
)
def get_current_rates(currency: str):
    """Get current conversion rates for the specified currency."""
    return make_request("GET", f"currency/rate", params={"currency": currency})


@tool(
    instructions="""
    Retrieve the minimum allowed amount for a specified currency. Example:
    get_minimum_allowed_amount(currency='USD')
    """
)
def get_minimum_allowed_amount(currency: str):
    """Get the minimum allowed amount for the specified currency."""
    return make_request("GET", "currency/minimum-allowed", params={"currency": currency})

@tool(
    instructions="""
    Retrieve a list of all supported currencies. Example:
    get_supported_currencies()
    """
)
def get_supported_currencies():
    """Get a list of all supported currencies."""
    return make_request("GET", "currency/supported")

@tool(
    instructions="""
    Retrieve a list of supported cryptocurrencies and networks. Example:
    get_supported_cryptocurrencies()
    """
)
def get_supported_cryptocurrencies():
    """Get a list of all supported cryptocurrencies and networks."""
    return make_request("GET", "wallet/supported/config")

@tool(
    instructions="""
    Resolve an overpaid transaction by specifying the transaction ID and the desired option. Example:
    resolve_overpaid_transaction(transaction_id='txn123', option='refundExcess')
    """
)
def resolve_overpaid_transaction(transaction_id: str, option: str):
    """Resolve an overpaid transaction with the specified option ('refundExcess' or 'payAll')."""
    params = {"id": transaction_id, "option": option}
    return make_request("GET", "payment/resolve", params=params)


@tool(
    instructions="""
    Retrieve the currently subscribed webhook URL for your account. Example:
    get_subscribed_webhook_url()
    """
)
def get_subscribed_webhook_url():
    """Get the subscribed webhook URL."""
    return make_request("GET", "callbackurl")


@tool(
    instructions="""
    Retrieve transaction records for a user, with options for currency, type, page, limit, and duration. Example:
    get_transaction_records(currency='USD', type='deposit', page=1, limit=10, duration=30)
    """
)
def get_transaction_records(currency: str = None, type: str = None, page: int = None, limit: int = None, duration: int = None):
    """Get transaction records for a user with specified filters."""
    params = {
        "currency": currency,
        "type": type,
        "page": page,
        "limit": limit,
        "duration": duration
    }
    # Filter out None values
    params = {key: value for key, value in params.items() if value is not None}
    return make_request("GET", "transaction", params=params)


@tool(
    instructions="""
    Retrieve a transaction summary for a user with optional filters like currency, type, page, limit, and duration. Example:
    get_transaction_summary(currency='USD', type='deposit', page=1, limit=10, duration=30)
    """
)
def get_transaction_summary(currency: str = None, type: str = None, page: int = None, limit: int = None, duration: int = None):
    """Get a transaction summary for the user with specified filters."""
    params = {
        "currency": currency,
        "type": type,
        "page": page,
        "limit": limit,
        "duration": duration
    }
    # Filter out None values
    params = {key: value for key, value in params.items() if value is not None}
    return make_request("GET", "transaction/summary", params=params)


@tool(
    instructions="""
    Retrieve the wallet address for a specific cryptocurrency and network. Example:
    get_crypto_wallet_address(currency='BTC', network='mainnet')
    """
)
def get_crypto_wallet_address(currency: str, network: str):
    """Get the user's wallet address for the specified cryptocurrency and network."""
    params = {"currency": currency, "network": network}
    return make_request("GET", "wallet", params=params)


@tool(
    instructions="""
    Transfer cryptocurrency from one wallet to another. Example:
    wallet_transfer(network='mainnet', currency='BTC', address='wallet_address', amount=0.1, wallet_type='hot', memo='For services')
    """
)
def wallet_transfer(network: str, currency: str, address: str, amount: float, wallet_type: str = None, memo: str = None):
    """Transfer crypto from one wallet to another on the specified network."""
    data = {
        "network": network,
        "currency": currency,
        "address": address,
        "amount": amount,
        "walletType": wallet_type,
        "memo": memo
    }
    # Remove None values
    data = {key: value for key, value in data.items() if value is not None}
    return make_request("POST", "wallet/transfer", json=data)


@tool(
    instructions="""
    Transfer funds from your balance to another user by specifying the receiver's username, currency, amount, OTP token, and optional memo. Example:
    transfer_funds(receiver_username='user123', currency='USD', amount=50.0, token='123456', otp_type='otp', memo='Payment')
    """
)
def transfer_funds(receiver_username: str, currency: str, amount: float, token: str, otp_type: str, memo: str = None):
    """Transfer funds to another user."""
    data = {
        "receiverUsername": receiver_username,
        "currency": currency,
        "amount": amount,
        "token": token,
        "otpType": otp_type,
        "memo": memo
    }
    # Remove None values
    data = {key: value for key, value in data.items() if value is not None}
    return make_request("POST", "balance/transfer", json=data)


@tool(
    instructions="""
    Subscribe to a webhook by specifying a callback URL. Example:
    subscribe_to_webhook(callback_url='https://www.example.com/callback')
    """
)
def subscribe_to_webhook(callback_url: str):
    """Subscribe to a webhook with the specified callback URL."""
    data = {"callbackUrl": callback_url}
    return make_request("PUT", "callbackurl", json=data)


@tool(
    instructions="""
    Retrieve a transaction summary for a user with optional filters like currency, type, page, limit, and duration. Example:
    get_transaction_summary(currency='USD', type='deposit', page=1, limit=10, duration=30)
    """
)
def get_transaction_summary(currency: str = None, type: str = None, page: int = None, limit: int = None, duration: int = None):
    """Get a transaction summary for the user with specified filters."""
    params = {
        "currency": currency,
        "type": type,
        "page": page,
        "limit": limit,
        "duration": duration
    }
    params = {key: value for key, value in params.items() if value is not None}
    return make_request("GET", "transaction/summary", params=params)

@tool(
    instructions="""
    Retrieve the account balance for a specified currency, or all currencies if none specified. Example:
    get_account_balance(currency='USD')
    """
)
def get_account_balance(currency: str = None):
    """Get user's account balance for a specific currency or all currencies if not specified."""
    params = {"currency": currency} if currency else {}
    return make_request("GET", "balance", params=params)


@tool(
    instructions="""
    Off ramp crypto. Example:
    create_payment(business_id='biz123', incoming_amount=100.0, outgoing_amount=95.0, 
                   incoming_currency='USD', outgoing_currency='NGN', customer_email='customer@example.com', 
                   payment_type='bank', country='NG', account_number='123456789', account_name='John Doe', 
                   bank='Some Bank', bank_code='001')
    """
)
def off_ramp(
    business_id: str, incoming_amount: float, outgoing_amount: float,
    incoming_currency: str, outgoing_currency: str, customer_email: str,
    payment_type: str, reference: str = None, rate_key: str = None,
    coinprofile_username: str = None, country: str = None, account_number: str = None,
    account_name: str = None, bank: str = None, bank_code: str = None, currency: str = None
):
    """Resolve bank account"""
    bank_resolved = make_request("GET", f"currency/rate", params={"currency": currency})

    """Get current conversion rates for the specified currency."""
    currency_rate = make_request("GET", f"currency/rate", params={"currency": currency})

    """Create a payment transaction."""
    data = {
        "businessId": business_id,
        "incomingAmount": incoming_amount,
        "outgoingAmount": outgoing_amount,
        "incomingCurrency": incoming_currency,
        "outgoingCurrency": outgoing_currency,
        "customerEmail": customer_email,
        "paymentType": payment_type,
        "reference": reference,
        "rateKey": rate_key,
        "coinprofileUsername": coinprofile_username,
        "country": country,
        "accountNumber": account_number,
        "accountName": account_name,
        "bank": bank,
        "bankCode": bank_code,
    }
    # Filter out None values
    data = {key: value for key, value in data.items() if value is not None}
    return make_request("POST", "payment", json=data)


@tool(
    instructions="""
    Verify a bank account by providing the account number and bank code. Example:
    resolve_bank_account(account_number='123456789', bank_code='001')
    """
)
def resolve_bank_account(account_number: str, bank_code: str):
    """Verify a bank account and retrieve its details."""
    data = {"accountNumber": account_number, "bankCode": bank_code}
    return make_request("POST", "bank/resolve", json=data)


@tool(
    instructions="""
    Withdraw funds from the user’s balance by specifying account details, currency, amount, OTP, and bank information. Example:
    withdraw_balance(account_number='123456789', account_name='John Doe', bank='Bank Name', bank_code='001', currency='USD', amount=100.0, token='123456', otp_type='otp')
    """
)
def withdraw_balance(account_number: str, account_name: str, bank: str, bank_code: str, currency: str, amount: float, token: str = None, otp_type: str = None):
    """Withdraw funds from the user's balance with specified bank and OTP details."""
    data = {
        "accountNumber": account_number,
        "accountName": account_name,
        "bank": bank,
        "bankCode": bank_code,
        "currency": currency,
        "amount": amount,
        "token": token,
        "otpType": otp_type
    }
    # Remove None values
    data = {key: value for key, value in data.items() if value is not None}
    return make_request("POST", "balance/withdraw", json=data)


# Register tools
partna_tools = [
    retrieve_merchant_balance,
    retrieve_merchant_record,
    update_merchant_record,
    make_mock_payment,
    # off ramp
    create_payment,
    get_payment_by_id,
    get_transaction_by_id,
    get_current_rates,
    get_minimum_allowed_amount,
    get_supported_currencies,
    get_supported_cryptocurrencies,
    resolve_overpaid_transaction,
    get_subscribed_webhook_url,
    get_transaction_records,
    get_transaction_summary,
    get_crypto_wallet_address,
    # payout
    wallet_transfer,
    transfer_funds,
    subscribe_to_webhook,
    resolve_bank_account,
    get_transaction_summary,
    get_account_balance
]
