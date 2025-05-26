# Import your app's Order model
from order.models import Order as OrderModel
from .Format import Format
from .PaycomException import PaycomException
import telebot

bot = telebot.TeleBot('5340212657:AAFsp2rouKhb-TKGu7V51iYjUVu6d4wPdx0')

class Order:
    STATE_AVAILABLE = 1
    STATE_WAITING_PAY = 2
    STATE_PAY_ACCEPTED = 3
    STATE_DELIVERED = 4
    STATE_CANCELLED = 0

    # If order will not be validated, set and return this error message
    response_message = None

    def __init__(self, request_id):
        self.request_id = request_id

    def validate(self, account_params):
        account = account_params["account"]
        order_id_str = "order"
        amount_str = "amount"
        

        if (
                order_id_str not in account
                or account[order_id_str] == ""
                or Format.is_not_numeric(value=account[order_id_str])
        ):
            self.response_message = {
                "code": PaycomException.ERROR_INVALID_ACCOUNT,
                "message": {
                    "ru": "Идентификатор заказа не существует.",
                    "uz": "Buyurtma raqami mavjud emas.",
                    "en": "Order id does not exist.",
                },
                "data": "order_id",
            }
            return False

        elif (
                amount_str not in account_params
                or account_params[amount_str] == ""
                or Format.is_not_numeric(value=account_params[amount_str])
        ):
            self.response_message = {
                "code": PaycomException.ERROR_INVALID_AMOUNT,
                "message": {
                    "ru": "Сумма заказа не существует.",
                    "uz": "Buyurtma narxi mavjud emas.",
                    "en": "Order amount does not exist.",
                },
                "data": "amount",
            }
            return False
        else:

            try:
                order_id = int(account[order_id_str])
                # customer = int(account[customer_id_str])
                amount = account_params[amount_str]
                order = OrderModel.objects.get(pk=order_id)

                bot.send_message(717324646,f"{order.id}, {order.status},Narxi {int(order.total_price)} {int(amount)} {self.STATE_AVAILABLE}")
                if int(order.status) != self.STATE_AVAILABLE:
                    self.response_message = {
                        "code": -31050,
                        "message": {
                            "ru": "Состояние заказа является недействительным.",
                            "uz": "Buyurtma holati to'g'ri emas.",
                            "en": "Order state is invalid.",
                        },
                        "data": "state",
                    }
                    return False
                elif order.payment_status == 1:
                    self.response_message = {
                        "code": PaycomException.ERROR_INVALID_AMOUNT,
                        "message": {
                            "ru": "Оплата за заказ произведена",
                            "uz": "Buyurtma uchun to'lov amalga oshirilgan",
                            "en": "Payment was made for the order",
                        },
                        "data": "state",
                    }
                    return False

                elif int(order.total_price) * 100  != int(amount) :
                    self.response_message = {
                        "code": PaycomException.ERROR_INVALID_AMOUNT,
                        "message": {
                            "ru": "Сумма заказа неверна.",
                            "uz": "Buyurtma narxi noto'g'ri.",
                            "en": "Incorrect amount.",
                        },
                        "data": "amount",
                    }
                    return False

                else:
                    self.response_message = {"allow": True}
                    return True
            except OrderModel.DoesNotExist:

                self.response_message = {
                    "code": PaycomException.ERROR_INVALID_ACCOUNT,
                    "message": {
                        "ru": "Заказ не найден.",
                        "uz": "Buyurtma topilmadi.",
                        "en": "Order not found.",
                    },
                    "data": {
                        "account":{
                            "order":f"{order_id}"
                        }
                    },
                }
                return False
