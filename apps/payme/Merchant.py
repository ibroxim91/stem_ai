from base64 import standard_b64decode

from .conf import config
from .PaycomException import PaycomException
from .Response import Response
import telebot

bot = telebot.TeleBot('5340212657:AAFsp2rouKhb-TKGu7V51iYjUVu6d4wPdx0')

class Merchant:
    conf = None
    header = None
    auth_data = None

    def __init__(self, conf, request):
        self.conf = conf
        self.header = request.META.get("HTTP_AUTHORIZATION", None)
        self.auth_data = self.header.split()[1] if self.header is not None else ""
      
    def authorize(self):
    
        if (
            config["login"] + ":" + config["key"]
            != standard_b64decode(self.auth_data).decode("utf-8")
            or self.header is None
        ):
            return False
            
        return True
