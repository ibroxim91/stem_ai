from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

signer = TimestampSigner()

def generate_token(telegram_id: int) -> str:
    return signer.sign(str(telegram_id))