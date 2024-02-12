from rest_framework import serializers
from . models import Order,OrderItems

class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        feilds = '__all__'
class OrderSerializers(serializers.ModelSerializer):
    orderitem= serializers.SerializerMethodField(method_name='get_order_items', read_only=True)
    class Meta:
        model= Order
        feilds= '__all__'
    def get_order_items(self,obj):
        order_items = obj.orderitems.all()
        serializers = OrderItemSerializers(order_items, many=True)
        return serializers.data