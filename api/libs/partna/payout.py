from api.libs.partna.helpers import make_request

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
