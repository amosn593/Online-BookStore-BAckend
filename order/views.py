import stripe

from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .mpesa import MpesaAccessToken, LipanaMpesaPpassword

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework_simplejwt import authentication
from rest_framework import status,  permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer


@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        print(serializer.validated_data['paid_amount'])
        try:

            access_token = MpesaAccessToken.access_token

            api_url = LipanaMpesaPpassword.api_URL
            headers = {"Authorization": "Bearer %s" % access_token}

            request_sent = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": 1,  # int(serializer.validated_data['paid_amount']),
                # replace with your phone number to get stk push
                "PartyA": serializer.validated_data['mpesa_number'],
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                # replace with your phone number to get stk push
                "PhoneNumber": serializer.validated_data['mpesa_number'],
                "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                "AccountReference": "Henry",
                "TransactionDesc": "Testing stk push"
            }

            resp = requests.post(api_url, json=request_sent, headers=headers)

            ResponseCode = json.loads(resp.text)["ResponseCode"]

            if(ResponseCode == '0'):

                try:
                    serializer.save(user=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception:

                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
