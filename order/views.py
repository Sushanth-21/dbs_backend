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
                price=int(request.data["price"])
                qty1=int(request.data["quantity"])
                orders=Order.objects.exclude(status="rejected").exclude(price__lt=price)
                n=len(orders)
                qty=qty1//n
                for o in orders:
                    if o.status=="rejected" or o.quantity==0:
                        continue
                    if o.type=="limit":
                        if o.price<price:
                            o.status="rejected"
                            o.save()
                            continue
                        if o.quantity>=qty:
                            o.quantity-=qty
                            o.executed_qty+=qty
                            qty1-=qty
                    else:
                        o.quantity-=qty
                        o.executed_qty+=qty
                        qty1-=qty
                    o.save()
                orders=sorted(orders,reverse=True,key=lambda x:x.price)
                i=0
                rem=qty1
                while rem!=0 and i<n:
                    if orders[i].quantity!=0 and orders[i].status!="rejected":
                        if orders[i].quantity<=rem:
                            rem-=orders[i].quantity
                            orders[i].executed_qty+=rem
                            orders[i].quantity=0
                        else:
                            tmp=orders[i].quantity
                            orders[i].quantity-=rem
                            orders[i].executed_qty+=rem
                            rem-=tmp
                        orders[i].save()
                    i+=1
                print(rem)
                return Response({"orders":Order.objects.all().values()},200)
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