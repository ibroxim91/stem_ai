import base64
from django.shortcuts import get_object_or_404,redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings 
from apps.order.models.order import Order, PaymentType
from apps.cauth.models.tariff import Tariff
from apps.order.serializers.order_serializer import OrderSerializer
from apps.clickuz.clickuz import ClickUz


class OrderCreateView(APIView):
    model = Order
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        print()
        print("data     ", data)
        print()
        payment_type = data.get('payment_type')
        if payment_type not in PaymentType.values:
            return Response({"error": "Payment  type must be one of ('click', 'stripe', 'payme')"}, status=400)
        self.tarif = data.get('tariff')
        self.order = self.model.objects.create(user=request.user, tariff=self.tarif, total_price=self.tarif.price,  payment_type=payment_type)
        if payment_type == 'click':
            return self.click_view()
        elif payment_type == 'stripe':
            return self.stripe_view()    
        else:    
            return self.payme_view()
            
    
    def click_view(self):
        url = ClickUz.generate_url(order_id=self.order.id, amount=  self.tarif.price,  return_url="https://5889-213-230-93-59.ngrok-free.app/api/v1/click/")
        return Response({
            "payment_url": url,
            "success": True,
             "message": ""
        })

    
    def stripe_view(self):
        return Response({
            "payment_url": None,
            "success": False,
            "message": "Stripe not implemented"
        })    

    def payme_view(self):
         return Response({
            "payment_url": None,
            "success": False,
            "message": "Payme not implemented"
        })   
        # # PAYCOM_MERCHANT_ID, PAYCOM_RETURN_URL
        # merchant = PAYME_SETTINGS['PAYCOM_MERCHANT_ID']
        # link = "https://checkout.paycom.uz"
        # return_url = PAYME_SETTINGS['PAYCOM_RETURN_URL'] 
        # total_amount = self.direct.price * 100
        # params = f"m={merchant};ac.order={self.order.id};a={total_amount};c={return_url}"
        # encode_params = base64.b64encode(params.encode("utf-8"))
        # encode_params = str(encode_params, "utf-8")
        # url = f"{link}/{encode_params}"
        # return HttpResponseRedirect(url)




# class PaymentView(APIView):
#     def post(self, request):
#         try:
#             app = paycom(request=request)
#             response = app.run()
#             data = json.loads(response)
#             return JsonResponse(data=data, safe=False)
#         except:
#             pass
#         return Response(status=status.HTTP_400_BAD_REQUEST)
# class UserPaymentCreateView(View):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, order):
#         user = self.request.user
#         order_obj = get_object_or_404(
#             Order.objects.filter(user_id=user.id), pk=order)
#         link = "https://checkout.paycom.uz"

#         merchant   = PAYME_SETTINGS['PAYCOM_MERCHANT_ID']
#         return_url = PAYME_SETTINGS['PAYCOM_RETURN_URL'] 

#         total_amount = order_obj.total_price * 100
#         params = f"m={merchant};ac.order_id={order};a={total_amount};c={return_url}"
#         encode_params = base64.b64encode(params.encode("utf-8"))
#         encode_params = str(encode_params, "utf-8")
#         url = f"{link}/{encode_params}"
#         return Response({"url": url}, status=status.HTTP_200_OK)



# class OrderCheckAndPayment(ClickUz):
#     def check_order(self, order_id: str, amount: str):
#         try:
#             order = Order.objects.get(id=int(order_id))
#         except:    
#             return self.ORDER_NOT_FOUND
#         if int(amount) != order.total_price:
#             return self.INVALID_AMOUNT
#         else:          
#             return self.ORDER_FOUND

#     def successfully_payment(self, order_id: str, transaction: object):
#         return True

# class ClickApiView(ClickUzMerchantAPIView):
#     VALIDATE_CLASS = OrderCheckAndPayment

