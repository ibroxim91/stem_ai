from .status import ORDER_FOUND, ORDER_NOT_FOUND, INVALID_AMOUNT
from django.conf import settings
from apps.order.models.order import Order

class ClickUz:
    ORDER_FOUND = ORDER_FOUND
    ORDER_NOT_FOUND = ORDER_NOT_FOUND
    INVALID_AMOUNT = INVALID_AMOUNT

    def check_order(self, order_id: str, amount: str):
        """
        :Need to check order
        :param order_id:
        :param amount:
        :return: ORDER_NOT_FOUND or ORDER_FOUND or INVALID_AMOUNT
        """
        try:
            order = Order.objects.get(id=int(order_id))
        except:    
            return self.ORDER_NOT_FOUND

        if int(amount) != order.total_price:
            
            return self.INVALID_AMOUNT
        else:          
            return self.ORDER_FOUND
        return self.ORDER_NOT_FOUND    


    def successfully_payment(self, order_id: str, transaction: object):
        """

        :param order_id:
        :return:
        """
        raise NotImplemented

    def cancel_payment(self, order_id: str, transaction: object):
        """
        ru: еще не добавлено отменить транзакцию
        en: not yet added cancel transaction
        :param order_id:
        :param transaction:
        :return:
        """
        pass

    @staticmethod
    def generate_url(order_id, amount, return_url=None):
        service_id = settings.CLICK_SETTINGS['service_id']
        merchant_id = settings.CLICK_SETTINGS['merchant_id']
        url = f"https://my.click.uz/services/pay?service_id={service_id}&merchant_id={merchant_id}&amount={amount}&transaction_param={order_id}"
        if return_url:
            url += f"&return_url={return_url}"
        return url
