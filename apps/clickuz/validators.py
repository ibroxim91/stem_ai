from apps.order.models.order import Order, OrderStatus, PaymentStatus
from .status import ORDER_FOUND, ORDER_NOT_FOUND, INVALID_AMOUNT


class OrderCheckAndPayment:
    def check_order(self, order_id: str, amount: str):
        try:
            order = Order.objects.get(id=int(order_id))
        except:    
            return ORDER_NOT_FOUND
        if int(amount) != order.total_price:
            return INVALID_AMOUNT
        else:          
            return ORDER_FOUND

    def successfully_payment(self, order_id, transaction): 
        try:
            order = Order.objects.get(id=int(order_id))
            order.status = OrderStatus.delivered
            order.payment_status = PaymentStatus.paid
            user = order.user
            user.is_active_user = True
            user.total_tokens += order.tariff.tokens
            user.save()
            order.save()
        except:    
            return ORDER_NOT_FOUND
         