from rest_framework import serializers
from .models import Product,Review

class ProductSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField(method_name='get_reviews',read_only=True)
    class Meta:
        model = Product
        fields= '__all__'
    def get_reviews(self,object):
        review = object.reviews.all()
        serializer= ReviewSerializer(review, many = True)
        return serializer.data
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields= '__all__'
        