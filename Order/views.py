from django.shortcuts import get_object_or_404,render
from .models import Order ,OrderItems
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import OrderItemSerializers,OrderSerializers
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from APIproduct.models import Product

@api_view(['GET'])
@permission_classes(IsAuthenticated)
def get_orders(request):
    order = Order.objects.all()
    serializers = OrderSerializers(order,many=True)
    return Response({'orders':serializers.data})

@api_view(['GET'])
@permission_classes(IsAuthenticated)
def get_order(request,pk):
    order = get_object_or_404(Order,id=pk)
    serializers = OrderSerializers(order,many=False)
    return Response({'order':serializers.data})

@api_view(['PUT'])
@permission_classes(IsAuthenticated,IsAdminUser)
def procces_orders(request,pk):
    order = get_object_or_404(Order,  id=pk)
    order.state = request.data['state']
    order.save()
    serializers = OrderSerializers(order,many=False)
    return Response({'orders':serializers.data})

@api_view(['DELETE'])
@permission_classes(IsAuthenticated)
def delete_order(request,pk):
    order = get_object_or_404(Order,  id=pk)
    order.state = request.data['state']
    order.delete()
    return Response({'details':'Order is deleted'})


@api_view(['POST'])
@permission_classes(IsAuthenticated)
def new_order(request):
    user = request.user
    data = request.data
    order_items= data['order_items']
    if order_items and len(order_items) == 0:
        return Response({'error':'No Order recieved'},status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount = sum(item['price']*item['quantity'] for item in order_items)
        order= Order.objects.create(
            user = user,
            city = data['city'],
            zip_code = data['zip_code'],
            street = data['street'],
            phone_no = data['phone_no'],
            country = data['country'],
            total_amount = total_amount 
        )
        for i in order_items:
            product = Product.objects.get(id=i['product'])
            item = OrderItems.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = i['quantity'],
                price = i['price']
            )
            product.stock -= item.quantity
            product.save()
        serializers = OrderSerializers(order,many=False)
        return Response(serializers.data)