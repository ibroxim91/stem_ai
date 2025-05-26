from django.conf import settings 
PAYME_SETTINGS = settings.PAYME_SETTINGS

config = {
    "merchantId": PAYME_SETTINGS['PAYCOM_MERCHANT_ID'],
    "login": "Paycom",
    "key": PAYME_SETTINGS['PAYCOM_KEY'],
}

account_params = {"userid"}
