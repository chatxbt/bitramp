import base64
import os
import rsa
from api.libs.db import get_supabase_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CurrencyRateRequest:
    currency: str


class CurrencyRateResponse(CurrencyRateRequest):
    pass

user_table_name = "users"
transaction_table_name = "transaction"


# Load Partna's RSA public key for signature verification
PARTNA_PUBLIC_KEY = rsa.PublicKey.load_pkcs1_openssl_pem(b"""
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA3huAlrgvx5sXAwH7rD/O
k3cKWh89qEQ6z0N8EeQQN5aaQQRREH6ptW3+r1aqum+co8urSdyAoO/n+b8OJR3v
acuX6xdX4Q3VG02FpDeclXKF6hii/WaxKqNg1wo+qEKKqWKO5l3eObYE6bWgEG1E
NEQ3o5JTpNj28tjUxjfcEzMf0b3OLzKNUKQCef75sTwghFwAVUqrcjqCXlcVihL9
G3XC98iTstZm/+kpG3krUmbFAYqNgGLOvAjsMViOQVjFBivg2XgeODxfidXn3VPz
QERvnULoDx05UWyRe+qJjCGgJSKYq0u4V3IuzNEL61zCwb8Nzi4Ng1EORvOTuJNO
W0nmtCH4ZhoSaPG86u4TWUnIK13A13I38HfguLB4hAMlqhCr8HhTPovsGZXsOOnI
OmueAe1V1ov/7mYwQ+G1Ccw4D8wIHVNdSKgNcEytkuAlhutzDRwsUVk0GBO75p3M
F2pQftz9CTgW0wjBLhTnJSDF4Ijn2VnPIYkNGJJ5IkAJJdRQgPkKJfQ5LE9ALkGi
KOC0e3uxanX9gNVv3DQ3SnlTgW/0KbaBbEF3AbjY4ui4jCq86LyBauGPjLb2lpfI
b85DkLcX6IyO24Mbe6q6x1SBCun6rPsBdzrm4lwanI95aqu0s9ytNsZbc2pGKDBC
HfN+y4hyWPZEYUCkZHmxymsCAwEAAQ==
-----END PUBLIC KEY-----
""")


def verify_signature(data, signature):
    """Verifies the RSA signature for the payload."""
    message = str(data).encode('utf-8')
    decoded_signature = base64.b64decode(signature)
    try:
        rsa.verify(
            message,
            decoded_signature,
            PARTNA_PUBLIC_KEY
        )
        return True
    except rsa.VerificationError:
        return False


# Event processing functions
def process_payment_created(data):
    print("Payment Created:", data)


async def process_payment_updated(data):
    print("Payment Updated:", data)
    supabase = await get_supabase_client()

    # find transaction with reference
    tnx = await supabase.from_(user_table_name) \
        .select("*") \
        .eq("reference", data["reference"]) \
        .single() \
        .execute()

    # update transaction record
    tnx_updated = (
        supabase.table(user_table_name)
        .update({"status": True})
        .eq("reference", data["reference"])
        .execute()
    )


def process_transaction_updated(data):
    print("Transaction Updated:", data)
