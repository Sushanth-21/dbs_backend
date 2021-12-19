from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions,authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Order,Market
import datetime


class orderStock(APIView):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]

    def post(self,request):
        try:
            m,c=Market.objects.get_or_create(id=1)
            if m.status=="True":
                stock=request.data["stock_name"]
                qty=request.data["quantity"]
                type=request.data["type"]
                exc=request.data["executed_qty"]
                price=request.data["price"]
                status=request.data["status"]
                date=datetime.datetime.strptime(request.data["date"],"%Y-%m-%d").date()
                order=Order.objects.create(ordered_by=request.user,stock_name=stock,quantity=int(qty),type=type,executed_qty=int(exc),price=int(price),date=date,status=status)
                return Response({"message":"placed"},200)
            else:
                return Response({"message":"Currently the market is closed. Please try ordering after market is opened."},400)
        except Exception as e:
            return Response({"error":str(e)},400)

class execute(APIView):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]

    def post(self,request):
        try:
            m,c=Market.objects.get_or_create(id=1)
            if m.status=="True":
                pass
            else:
                return Response({"message":"You don't have the permission to execute the orders."},400)
        except Exception as e:
            return Response({"error":str(e)},400)


class market(APIView):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]

    def post(self,request):
        try:
            m,c=Market.objects.get_or_create(id=1)
            if request.user.is_staff:
                st=False
                if request.data["status"]=="true":
                    st=True
                m.status=st
                m.save()
            else:
                return Response({"error":"Current user doesn't have permisions to open/close the market"},400)
            return Response({"status":m.status},200)
        except Exception as e:
            return Response({"error":str(e)},400)